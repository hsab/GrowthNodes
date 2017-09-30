'''
Copyright (C) 2016 Jacques Lucke
mail@jlucke.com

Created by Jacques Lucke

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
Command Line Arguments:
    python setup.py
     --all              # clean, comment pyximport and recompile all
     --export           # make redistributable version
     --copy             # copy the build into Blenders addon directory
     --clean            # removes .c, .pyd, .so, and .zip files as well as build folder and __pycache__ folders
     --pyximport        # for building Cython modules during development without explicitly
                        # running setup.py after each change. Unomments the following across all files
                        #     import pyximport
                        #     pyximport.install()
     --noversioncheck   # allow to create a build with any Python version

Generate .html files to debug cython code:
    cython -a path/to/file.pyx

Cleanup Repository:
    git clean -fdx       # make sure you don't have uncommited files!
'''

import os
import sys
import shutil
import traceback
from os.path import abspath, dirname, join, relpath
import textwrap
import numpy

addonName = "umog_addon"
currentDirectory = dirname(abspath(__file__))
sourceDirectory = join(currentDirectory, addonName)
#sourceDirectory = currentDirectory
configPath = join(currentDirectory, "config.py")
defaultConfigPath = join(currentDirectory, "config.default.py")
compilationInfoPath = join(sourceDirectory, "compilation_info.json")

config = {}

initialArgs = sys.argv[:]

expectedArgs = {"--all", "--export", "--copy", "--clean", "--noversioncheck", "--pyximport"}
unknownArgs = set(initialArgs[1:]) - expectedArgs

textWidth = 48

def printFunc(operation, description, output):
    width = '{:^'+str(textWidth-5)+'}'
    print()
    print("+---------------------------------------------+")
    print("|", width.format(operation), "|")
    print("+---------------------------------------------+")
    print(textwrap.fill(description, textWidth))

    if output:
        print()
        print(operation, "OUTPUT:")

def printInd(message):
    wrapper = textwrap.TextWrapper(initial_indent="---- ", width=textWidth*3)
    print(wrapper.fill(message))

if len(unknownArgs) > 0:
    printFunc("UNKNOWN ARGUMENTS", "Unknown arguments have been detected.", True)
    printInd("Unknown arguments:"+ str(unknownArgs))
    printInd("Allowed arguments:"+ str(expectedArgs))
    sys.exit()

v = sys.version_info
if "--noversioncheck" not in initialArgs and (v.major != 3 or v.minor != 5):
    message = "Blender 2.78/2.79 officially uses Python 3.5.x.\n" + "You are using: {}".format(sys.version)
    printFunc("PYTHON VERSION", message, False)
    printInd("Use the --noversioncheck argument to disable this check.")
    sys.exit()
else:
    printFunc("PYTHON VERSION", sys.version, False)

def main():
    if "--clean" in initialArgs:
        printFunc("--CLEAN", "It is not possible to combine the \"--clean\" argument with other arguments.", True)
        clean()
        return

    if "--pyximport" in initialArgs:
        printFunc("--PYXIMPORT", "Allows for building Cython modules during development without explicitly running setup.py after each change", True)
        clean()
        commentPyximport(".py", sourceDirectory, False)
        writePyximportInfoFile()
        return

    initFileHack(currentDirectory, ".py", ".temp")

    printFunc("SETUP CONFIG", "Used to specify where the compiled addon should be copied, what files, and folders should be excluded.", True)
    setupAndReadConfigFile()

    if canCompile():
        print("\nPYXIMPORT:")
        commentPyximport(".py", sourceDirectory, True)
        preprocessor()
        if "--all" in initialArgs:
            printFunc("--ALL", "Recompiles all files, by removing .c, .pyd, .so, and .zip files from the directory.", True)
            clean()
        compileCythonFiles()
        writeCompilationInfoFile()
        if "--export" in initialArgs:
            printFunc("--EXPORT", "Creates a zip file that can be shared with others.", True)
            export()
        if "--copy" in initialArgs:
            printFunc("COPY TO BLENDER", "Copies the compiled addon to Blender addon directory.", True)

            if os.path.isdir(config["addonsDirectory"]):
                copyToBlender()
            else:
                printInd("The path to Blenders addon directory does not exist")
                printInd("Please correct the config.py file.")

    initFileHack(currentDirectory, ".temp", ".py")

def setupAndReadConfigFile():
    if not os.path.isfile(configPath) and os.path.isfile(defaultConfigPath):
        shutil.copyfile(defaultConfigPath, configPath)
        printInd("Copied the config.default.py file to config.py")
        printInd("Please change it manually if needed.")
        printInd("Note: git ignores it, so depending on the settings of your editor")
        printInd("      it might not be shown inside it.\n\n")

    if os.path.isfile(configPath):
        configCode = readFile(configPath)
        exec(configCode, config, config)
    else:
        printInd("Cannot find any of these files: config.py, config.default.py ")
        printInd("Make sure that at least the config.default.py exists.")
        printInd("Maybe you have to clone the repository again.")
        sys.exit()

def canCompile():
    printFunc("COMPILE SANITY", "Tests different parameters & modules to endure compilation is possible.", True)
    if "bpy" in sys.modules:
        printInd("Found bpy in sys.modules")
        return False
    if not os.path.isdir(sourceDirectory):
        printInd("Addon directory",sourceDirectory, "does not exists")
        return False
    printInd("No issues found so far")
    print()
    print("CORRECTING SYSTEM PATHS:")
    correctSysPath()
    print()

    print("CHECKING CYTHON:")
    try:
        import Cython
        printInd("Cython successfully imported.")
        return True
    except:
        printInd("Cython is not installed for this Python version.")
        printInd(sys.version)
        return False

def correctSysPath():
    pathsToRemove = [path for path in sys.path if currentDirectory in path]
    for path in pathsToRemove:
        sys.path.remove(path)
        printInd("Removed from sys.path:"+ path)



# Preprocess - execute .pre files
###################################################################

def preprocessor():
    printFunc("PREPROCESSOR", "Executes .pre files by creating the appropriate context.", False)
    for path in iterPathsWithSuffix(".pre", sourceDirectory):
        code = readFile(path)
        codeBlock = compile(code, path, "exec")
        context = {
            "__file__" : abspath(path),
            "readFile" : readFile,
            "writeFile" : writeFile,
            "multiReplace" : multiReplace,
            "dependenciesChanged" : dependenciesChanged,
            "changeFileName" : changeFileName}
        exec(codeBlock, context, context)



# Translate .pyx to .c files and compile extension modules
###################################################################

def compileCythonFiles():
    printFunc("COMPILE", "Compilation starts at this point using build_ext and --inplace arguments.", True)

    from distutils.core import setup
    from Cython.Build import cythonize

    sys.argv = [sys.argv[0], "build_ext", "--inplace"]
    extensions = cythonize(getPathsToCythonFiles(sourceDirectory))
    setup(name = 'UMOG', ext_modules = extensions, include_dirs=[numpy.get_include()])
    printInd("Compilation Successful.")

def getPathsToCythonFiles(directory):
    return list(iterPathsWithSuffix(".pyx", directory))

def clean():
    for root, folders, files in os.walk(currentDirectory, topdown = True):
        for folder in folders:
            if folder.endswith("__pycache__"):
                path = os.path.join(os.path.abspath(root), folder)
                removeDirectory(path, "")

    removeDirectory(currentDirectory, "build")
    removeFilesWithSuffix(".c", sourceDirectory)
    removeFilesWithSuffix(".json", sourceDirectory)
    removeFilesWithSuffix(".so", sourceDirectory)
    removeFilesWithSuffix(".pyd", sourceDirectory)
    removeFilesWithSuffix(".zip", currentDirectory)

def removeFilesWithSuffix(extension, directory):
    for path in iterPathsWithSuffix(extension, directory):
        os.remove(path)
    printInd("Removed "+ extension+ " files.")


import fileinput
import re

def commentPyximport(extension, directory, comment):
    patternImp = re.compile(r'^import pyximport$', flags=re.M)
    patternImpCom = re.compile(r'^#import pyximport$', flags=re.M)
    patternInst = re.compile(r'^pyximport.install\(\)$', flags=re.M)
    patternInstCom = re.compile(r'^#pyximport.install\(\)$', flags=re.M)
    for path in iterPathsWithSuffix(extension, directory):
        for line in fileinput.input(path, inplace=True):
            modified = True
            if comment:
                if patternImp.search(line):
                    sys.stderr.write("---- Commented Line " + str(fileinput.filelineno()) + "\n")
                    print(re.sub(patternImp, "#import pyximport", line), end='')
                elif patternInst.search(line):
                    sys.stderr.write("---- Commented Line " + str(fileinput.filelineno()) + "\n")
                    print(re.sub(patternInst, "#pyximport.install()", line), end='')
                else:
                    print(line, end='')
                    modified=False
            else:
                if patternImpCom.search(line):
                    sys.stderr.write("---- Uncommented Line " + str(fileinput.filelineno()) + "\n")
                    print(re.sub(patternImpCom, "import pyximport", line), end='')
                elif patternInstCom.search(line):
                    sys.stderr.write("---- Unommented Line " + str(fileinput.filelineno()) + "\n")
                    print(re.sub(patternInstCom, "pyximport.install()", line), end='')
                else:
                    print(line, end='')
                    modified=False

            if modified:
                sys.stderr.write("----   @ " + path + "\n")

# Compilation Info File
###################################################################

def writeCompilationInfoFile():
    import Cython
    printFunc("JSON LOG", "Creates a compilation info log.", True)

    info = {}
    info["sys.version"] = sys.version
    info["sys.platform"] = sys.platform
    info["sys.api_version"] = sys.api_version
    info["sys.version_info"] = sys.version_info
    info["Cython.__version__"] = Cython.__version__
    info["os.name"] = os.name

    import json
    writeFile(compilationInfoPath, json.dumps(info, indent = 4))

def writePyximportInfoFile():
    printFunc("JSON LOG", "Creates a pyximport info log.", True)

    info = {}
    info["sys.pyximport"] = True

    import json
    writeFile(compilationInfoPath, json.dumps(info, indent = 4))

# Copy to Blenders addons directory
###################################################################

def copyToBlender():
    targetPath = join(config["addonsDirectory"], addonName)
    try:
        copyAddonFiles(sourceDirectory, targetPath, verbose = True)
    except PermissionError:
        traceback.print_exc()
        printInd("Maybe this error happens because Blender is running.")
        sys.exit()
    printInd("Copied all changes")



# Export Build
###################################################################

def export():
    printInd("Start Export")

    targetPath = join(currentDirectory, addonName + ".zip")
    zipAddonDirectory(sourceDirectory, targetPath)

    printInd("Finished Export")
    printInd("Zipped file can be found here:")
    printInd("  " + targetPath)



# Copy Addon Utilities
###################################################################

def copyAddonFiles(source, target, verbose = False):
    if not os.path.isdir(target):
        os.mkdir(target)

    existingFilesInSource = set(iterRelativeAddonFiles(source))
    existingFilesInTarget = set(iterRelativeAddonFiles(target))

    counter = 0

    filesToRemove = existingFilesInTarget - existingFilesInSource
    for relativePath in filesToRemove:
        path = join(target, relativePath)
        removeFile(path)
        if verbose: printInd("Removed File: ", path)
        counter += 1

    filesToCreate = existingFilesInSource - existingFilesInTarget
    for relativePath in filesToCreate:
        sourcePath = join(source, relativePath)
        targetPath = join(target, relativePath)
        copyFile(sourcePath, targetPath)
        if verbose: printInd("Created File: ", targetPath)
        counter += 1

    filesToUpdate = existingFilesInSource.intersection(existingFilesInTarget)
    for relativePath in filesToUpdate:
        sourcePath = join(source, relativePath)
        targetPath = join(target, relativePath)
        sourceModificationTime = os.stat(sourcePath).st_mtime
        targetModificationTime = os.stat(targetPath).st_mtime
        if sourceModificationTime > targetModificationTime:
            overwriteFile(sourcePath, targetPath)
            if verbose: printInd("Updated File: ", targetPath)
            counter += 1

    printInd("Changed {} files.".format(counter))

def removeFile(path):
    try:
        os.remove(path)
    except:
        if tryGetFileAccessPermission(path):
            os.remove(path)

def removeDirectory(path, folder):
    try:
        shutil.rmtree(path + "\\" + folder, ignore_errors=False, onerror=None)
        printInd("Removed folder:")
        printInd(" "+path)
    except:
        if tryGetFileAccessPermission(path):
            shutil.rmtree(path + folder, ignore_errors=False, onerror=None)

def copyFile(source, target):
    directory = dirname(target)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    shutil.copyfile(source, target)

def overwriteFile(source, target):
    removeFile(target)
    copyFile(source, target)


def iterRelativeAddonFiles(directory):
    if not os.path.isdir(directory):
        return

    for root, folders, files in os.walk(directory, topdown = True):
        for folder in folders:
            folders[:] = [d for d in folders if not ignoreAddonDirectory(d)] 

        for fileName in files:
            if not ignoreAddonFile(fileName):
                yield relpath(join(root, fileName), directory)


def ignoreAddonFile(name):
    if any(x in name for x in config["skipFiles"]):
        return True

    return name.endswith(".c") or name.endswith(".html")

def ignoreAddonDirectory(name):
    return name in config["skipFolders"]

def tryRemoveDirectory(path):
    try: shutil.rmtree(path, onerror = handlePermissionError)
    except FileNotFoundError: pass

def handlePermissionError(function, path, excinfo):
    if tryGetFileAccessPermission(path):
        function(path)
    else:
        raise

def tryGetFileAccessPermission(path):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        return True
    return False

def zipAddonDirectory(sourcePath, targetPath):
    try: os.remove(targetPath)
    except FileNotFoundError: pass

    import zipfile
    with zipfile.ZipFile(targetPath, "w", zipfile.ZIP_DEFLATED) as zipFile:
        for relativePath in iterRelativeAddonFiles(sourcePath):
            absolutePath = join(sourcePath, relativePath)
            zipFile.write(absolutePath, join(addonName, relativePath))


# Utils
###################################################################

def iterPathsWithSuffix(suffix, directory):
    for root, dirs, files in os.walk(directory):
        for fileName in files:
            if fileName.endswith(suffix):
                yield join(root, fileName)

# So that setup.py can properly compile.
# There are issues with having setup.py in the module folder
def initFileHack(directory, extFrom, extTo):
    for file in os.listdir(directory):
        if "__init__"+extFrom in file:
            printFunc("INIT RENAME", "In order to correctly compile the addon, __init__"+extFrom+" needs to be renamed.", True)
            printInd("Renamed __init__"+extFrom+" to __init__"+extTo)
            os.rename(file, "__init__"+extTo)


def writeFile(path, content):
    with open(path, "wt") as f:
        f.write(content)
    printInd("Changed File:"+ path)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def changeFileName(path, newName):
    return join(dirname(path), newName)

def multiReplace(text, **replacements):
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

def dependenciesChanged(target, dependencies):
    try: targetTime = os.stat(target).st_mtime
    except FileNotFoundError: targetTime = 0
    latestDependencyModification = max(os.stat(path).st_mtime for path in dependencies)
    return targetTime < latestDependencyModification

main()
