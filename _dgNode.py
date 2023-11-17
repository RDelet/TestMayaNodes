from typing import Union

from maya.api import OpenMaya

from TestMayaNodes import _factory, utils


@_factory.register()
class _DGNode:

    kApiType = OpenMaya.MFn.kDependencyNode

    def __init__(self, node: Union[str, OpenMaya.MObject]):
        self._object = utils.check_object(node)
        self._mfn = None
        self._modifier = None
    
    def _post_init(self):
        self._mfn = OpenMaya.MFnDependencyNode(self._object)
        self._modifier = OpenMaya.MDGModifier()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name}, type: {self.type})"
    
    @property
    def api_type(self) -> int:
        return self.object.apiType

    @property
    def mfn(self):
        return self._mfn
    
    @property
    def modifier(self) -> OpenMaya.MDGModifier:
        return self._modifier

    @property
    def name(self):
        return utils.name(self._object)

    @property
    def object(self) -> OpenMaya.MObject:
        return self._object
    
    @property
    def short_name(self):
        return utils.name(self._object, False, False)
    
    @property
    def type(self) -> str:
        return self.object.apiTypeStr
