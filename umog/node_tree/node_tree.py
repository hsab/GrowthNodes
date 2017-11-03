from ..engine import engine
import bpy
from bpy.types import NodeTree
from collections import defaultdict

class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    def execute(self):
        print('Executing node tree')

        nodes = self.topological_sort()
        eng = engine.Engine(nodes)
        eng.run()

    # returns [(node, [(node_index, socket_index)])]
    def topological_sort(self):
        permanent = defaultdict(lambda: False)
        temporary = defaultdict(lambda: False)

        nodes = []

        def visit(node):
            if permanent[node.name]:
                return
            if temporary[node.name]:
                raise CyclicNodeGraphError()

            temporary[node.name] = True

            input_indices = []
            for input in node.inputs:
                if len(input.links) == 0:
                    input_indices.append(None)
                else:
                    index = visit(input.links[0].from_node)
                    input_indices.append((index, list(input.links[0].from_node.outputs).index(input.links[0].from_socket)))

            permanent[node.name] = True

            index = len(nodes)
            nodes.append((node, input_indices))
            return index

        for node in self.nodes:
            if node._IsOutputNode:
                visit(node)

        return nodes

class CompilationError(Exception):
    pass

class CyclicNodeGraphError(CompilationError):
    pass
