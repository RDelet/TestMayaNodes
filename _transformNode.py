from maya.api import OpenMaya

from TestMayaNodes import _factory
from TestMayaNodes._dagNode import _DAGNode


@_factory.register()
class _TransformNode(_DAGNode):

    kApiType = OpenMaya.MFn.kTransform
