# encoding: utf-8
from __future__ import unicode_literals

import sys
import os

from ..preferences import getDeveloperSettings

def DBG(*messages, **options):
    try:
        isTraceEnabled = getDeveloperSettings().traceInfo
        isExecutionInfoEnabled = getDeveloperSettings().executionInfo
    except:
        return
    
    executionInfoExists = False

    if isTraceEnabled or isExecutionInfoEnabled:
        print()

    if isExecutionInfoEnabled and len(messages)>0:
        executionInfoExists = True
        
        notifier = getFunctionInfo(1)
        print("|||||||||",
            notifier["name"],
            "{ MESSAGE",
            notifier["executedLine"],
            "IN",
            notifier["path"],
            notifier["firstLine"],
            "}"
            )
        
        for message in messages:
            print("--------|", message)
        

    trace = True
    if "TRACE" in options:
        trace = options["TRACE"]

    if isExecutionInfoEnabled and isTraceEnabled and trace and executionInfoExists:
        print("        |")
    elif isExecutionInfoEnabled and executionInfoExists:
        print()

    if isTraceEnabled and trace:

        try:
            callee = getFunctionInfo(1)
            caller = getFunctionInfo(2)
        except: 
            callee = getFunctionInfo(0)
            caller = getFunctionInfo(1)

        traceData = [
            ["********|",    callee["name"],    '',                     callee["firstLine"],    callee["path"]],
            ['    FROM|',    caller["name"],    caller["executedLine"], caller["firstLine"],    caller["path"]]
        ]
        
        prettyPrint(traceData)
        print()
        
        argData = []

        for i in range(callee["frame"].f_code.co_argcount):
            argName = str(callee["frame"].f_code.co_varnames[i])
            argVal = str(callee["frame"].f_locals[argName])
            if i is 0:
                argData.append(["         ", argName, argVal])
            else:
                argData.append(['', argName, argVal])

        prettyPrint(argData)
        print()

def getFunctionInfo(frameNumber):
    frame = sys._getframe(frameNumber+1)

    functionObject = {
        "frame": frame,
        "path": str(frame.f_code.co_filename).split("umog_addon")[1],
        "name": str(frame.f_code.co_name),
        "executedLine": '@'+str(frame.f_lineno),
        "firstLine": '#'+str(frame.f_code.co_firstlineno)
    }
    
    return functionObject

def prettyPrint(table):
    widths = [max(map(len, col)) for col in zip(*table)]
    for row in table:
        print (
            "  ".join((val.ljust(width) for val, width in zip(row, widths)))
            )