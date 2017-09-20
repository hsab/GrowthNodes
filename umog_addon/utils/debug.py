# encoding: utf-8
from __future__ import unicode_literals

import sys
import os

def prettyPrint(table):
    widths = [max(map(len, col)) for col in zip(*table)]
    for row in table:
        print (
            "  ".join((val.ljust(width) for val, width in zip(row, widths)))
            )

def debugTrace():
    print()

    callee = sys._getframe(2)
    caller = sys._getframe(3)
    
    calleePath = str(callee.f_code.co_filename).split("umog_addon")
    calleeName = str(callee.f_code.co_name)
    calleeFirstLine = '#'+str(callee.f_code.co_firstlineno)

    callerPath = str(caller.f_code.co_filename).split("umog_addon")
    callerName = str(caller.f_code.co_name)
    callerExecutedLine = '@'+str(caller.f_lineno)
    callerFirstLine = '#'+str(caller.f_code.co_firstlineno)

    traceData = [
        ["--------|",    calleeName,    '',                  calleeFirstLine,    calleePath[1]],
        ['    FROM|',    callerName,    callerExecutedLine,  callerFirstLine,    callerPath[1]]
    ]
    
    prettyPrint(traceData)
    print()
    
    argData = []

    for i in range(callee.f_code.co_argcount):
        argName = str(callee.f_code.co_varnames[i])
        argVal = str(callee.f_locals[argName])
        if i is 0:
            argData.append(["         ", argName, argVal])
        else:
            argData.append(['', argName, argVal])

    prettyPrint(argData)
    print()