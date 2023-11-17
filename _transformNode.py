from typing import Union

from maya import OpenMaya

from Nodes._factory import _Factory
from Nodes._dagNode import _DAGNode


@_Factory.register()
class _TransformNode(_DAGNode):

    kApiType = OpenMaya.MFn.kTransform
