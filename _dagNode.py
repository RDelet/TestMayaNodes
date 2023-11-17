from typing import Union

from maya import OpenMaya

from Nodes._factory import _Factory
from Nodes.node import _AbstractNode


@_Factory.register()
class _DAGNode(_AbstractNode):

    kApiType = OpenMaya.MFn.kDagNode

    def __init__(self, node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath]):
        super(_DAGNode, self).__init__(node)
        self._mfn = OpenMaya.MFnDagNode(self._object)
    
    @property
    def mfn(self) -> OpenMaya.MFnDependencyNode:
        return self._mfn

    @property
    def name(self) -> str:
        return self.mfn.fullPathName()