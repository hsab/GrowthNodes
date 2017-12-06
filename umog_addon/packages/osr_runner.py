import sys
import os

def runner(cr):
    cr.run()
    cr.cleanUP()
    if sys.platform != "win32":
        cr.close()
        
def path_changer():
    cpath = os.path.dirname(os.path.realpath(__file__))
    print(cpath)
    cpath = os.path.split(cpath)[0]
    #cpath = os.path.split(cpath)[0]
    #cpath = os.path.split(cpath)[0]
    cpath = os.path.join(cpath, "packages")
    print(cpath)
    if cpath not in sys.path:
        sys.path.append(cpath)
