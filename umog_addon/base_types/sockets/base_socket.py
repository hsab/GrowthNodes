import bpy
from bpy.props import *
from collections import defaultdict

class UMOGSocket:
    storable = True
    comparable = False
    _isAnimationNodeSocket = True

    @classmethod
    def isCopyable(self):
        return hasattr(self, "getCopyExpression")

    @classmethod
    def getCopyExpression(cls):
        return "value[:]"