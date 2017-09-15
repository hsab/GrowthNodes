import bpy
from bpy.types import NodeTree

class UMOGNodeTree(NodeTree):
    bl_idname = "umog_UMOGNodeTree"
    bl_label = "UMOG"
    bl_icon = "SCULPTMODE_HLT"

    def execute(self, refholder):
        print('Executing node tree')

        start_nodes = []
        #initialize NodePriority to -1 for non output and 0 for output nodes
        nn2p = {}
        #dictionary of enabled
        nn2e = {}
        for node in self.nodes:
            try:
                if node._OutputNode:
                    nn2p[node.name] = 0
                    start_nodes.append(node)
            except:
                nn2p[node.name] = -1
            nn2e[node.name] = True
        
        #now using the start nodes
        while len(start_nodes) != 0:
            next_nodes = []
            for node in start_nodes:
                for ln in node.inputs:
                    try:
                        ln = ln.links[0].from_node
                        if nn2p[ln.name] != 0:
                            nn2p[ln.name] = nn2p[node.name] +1
                            next_nodes.append(ln)
                    except:
                        pass
            start_nodes = next_nodes
        #sort the nodes by NodePriority
        sorted_nodes = sorted(bpy.context.space_data.edit_tree.nodes, key=lambda node:nn2p[node.name])
        #highest numbered nodes should be first
        sorted_nodes.reverse()
        
        for node in sorted_nodes:
            if nn2p[node.name] == -1:
                nn2e[node.name] = False
        
        for node in sorted_nodes:
            if nn2e[node.name]:
                node.preExecute(refholder)
        for frames in range(bpy.context.scene.StartFrame, bpy.context.scene.EndFrame):
            for subframes in range(0, bpy.context.scene.SubFrames):
                for node in sorted_nodes:
                    if nn2e[node.name]:
                        node.execute(refholder)
            for node in sorted_nodes:
                if nn2e[node.name]:
                    node.postFrame(refholder)
                    #consider at what point to do the end of frame calls
        for node in sorted_nodes:
            if nn2e[node.name]:
                node.postBake(refholder)
