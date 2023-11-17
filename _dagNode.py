from maya.api import OpenMaya

from TestMayaNodes import _factory, utils
from TestMayaNodes._dgNode import _DGNode


@_factory.register()
class _DAGNode(_DGNode):

    kApiType = OpenMaya.MFn.kDagNode
    
    def _post_init(self):
        self._mfn = OpenMaya.MFnDagNode(utils.get_path(self._object))
        self._modifier = OpenMaya.MDagModifier()
