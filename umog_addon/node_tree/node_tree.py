import bpy
from bpy.types import NodeTree

from collections import defaultdict

class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    def execute(self, refholder, start_frame, end_frame, sub_frames, write_keyframes=False):
        print('Executing node tree')

        nodes = self.topological_sort()
        
        for node in nodes:
            node.preExecute(refholder)
            if write_keyframes and node._IsOutputNode:
                node.write_keyframe(refholder, start_frame)

        for frame in range(start_frame + 1, end_frame + 1):
            for sub_frame in range(0, sub_frames):
                for node in nodes:
                    node.execute(refholder)

            for node in nodes:
                node.postFrame(refholder)
                if write_keyframes and node._IsOutputNode:
                    node.write_keyframe(refholder, frame)

        for node in nodes:
            node.postBake(refholder)

    def topological_sort(self):
        stack = []
        nodes = []
        visited = defaultdict(lambda: False)

        # initialize stack with output nodes
        for node in self.nodes:
            if node._IsOutputNode:
                stack.append(node)
                nodes.append(node)
                visited[node.name] = True

        # perform a breadth-first traversal of the node graph
        while len(stack) > 0:
            node = stack.pop()
            for input in node.inputs:
                for link in input.links:
                    if not visited[link.from_node.name]:
                        stack.append(link.from_node)
                        nodes.append(link.from_node)
                        visited[link.from_node.name] = True

        return nodes
