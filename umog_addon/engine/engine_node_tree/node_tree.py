import bpy
from bpy.types import NodeTree
from bpy.props import *
from collections import defaultdict

from ..engine import engine
from ..engine import types

class EngineNodeTree(NodeTree):
    bl_idname = "engine_EngineNodeTree"
    bl_label = "Engine"
    bl_icon = "SCULPTMODE_HLT"

    def run(self):
        print('Executing node tree')

        nodes = self.topological_sort()
        eng = engine.Engine(nodes)
        eng.run()

    # returns [(node, [(node_index, socket_index)])]
    def topological_sort(self):
        permanent = defaultdict(lambda: None)
        temporary = defaultdict(lambda: False)

        nodes = []

        def visit(node):
            if permanent[node.name]:
                return permanent[node.name]
            if temporary[node.name]:
                raise types.CyclicNodeGraphError()

            temporary[node.name] = True

            input_indices = []
            for input in node.inputs:
                if len(input.links) == 0:
                    input_indices.append(None)
                else:
                    index = visit(input.links[0].from_node)
                    input_indices.append((index, list(input.links[0].from_node.outputs).index(input.links[0].from_socket)))

            index = len(nodes)
            nodes.append((node, input_indices))
            permanent[node.name] = index
            temporary[node.name] = False

            return index

        for node in self.nodes:
            if node._IsOutputNode:
                visit(node)

        return nodes
