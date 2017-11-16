import sys

def runner(cr):
    cr.run()
    cr.cleanUP()
    if sys.platform != "win32":
        cr.close()