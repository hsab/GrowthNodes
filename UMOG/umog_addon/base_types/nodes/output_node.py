from .umog_node import UMOGNode

class UMOGOutputNode(UMOGNode):
    _IsUMOGOutputNode = True

    def init(self, context):
        super().init(context)

    def write_keyframe(self, refholder, frame):
        pass
