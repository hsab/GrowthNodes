import os
import pkgutil
import importlib
from os.path import join

def importAllSubmodules(path, packageName, addonDirecotry):
    modules = []
    path = join(path, addonDirecotry)
    for name in sorted(iterSubModuleNames(path)):
        try:
            module = importlib.import_module("." + addonDirecotry + "." + name, packageName)
            modules.append(module)
        except:
            print("FAILED TO LOAD\t" + "." + addonDirecotry + "." + name, packageName)
            raise

    return modules

def iterSubModuleNames(path, root = ""):
    for importer, moduleName, isPackage in pkgutil.iter_modules([path]):
        if isPackage:
            subPath = os.path.join(path, moduleName)
            subRoot = root + moduleName + "."
            yield from iterSubModuleNames(subPath, subRoot)
        else:
            yield root + moduleName
