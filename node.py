# coding=ascii

from typing import Union

from maya import cmds, OpenMaya

from Nodes._factory import _Factory


class _AbstractNode(object):

    __msl = OpenMaya.MSelectionList()

    kApiType = -1

    def __init__(self, node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath]):
        self._object = node
        self._mfn = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name}, type: {self.type})"
    
    @property
    def object(self) -> OpenMaya.MObject:
        return self._object
    
    def force_update_object(self, node: OpenMaya.MObject):
        self._object = node

    @property
    def api_type(self) -> int:
        return self.object.apiType()
    
    @property
    def type(self) -> str:
        return self.object.apiTypeStr()

    @property
    def mfn(self):
        raise NotImplementedError(f"{self.__class__.__name__}.mfn need to be re-implemented !")
    
    @property
    def name(self):
        raise NotImplementedError(f"{self.__class__.__name__}.name need to be re-implemented !")

    @classmethod
    def exists(cls, node_name: str) -> bool:
        return cmds.objExists(node_name)

    @classmethod
    def get_object(cls, node_name: str) -> OpenMaya.MObject:
        if not cls.exists(node_name):
            raise RuntimeError(f"Object {node_name} does not exists !")

        cls.__msl.clear()
        cls.__msl.add(node_name)
        obj = OpenMaya.MObject()
        cls.__msl.getDependNode(0, obj)
        return obj


class Node(object):
    
    __dag_modifier = OpenMaya.MDagModifier()
    __dg_modifier = OpenMaya.MDGModifier()

    def __new__(self, node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath]):
        if isinstance(node, str):
            node = _AbstractNode.get_object(node)
        elif isinstance(node, OpenMaya.MDagPath):
            node = node.node()

        return _Factory.create(node)
    
    @classmethod
    def _inherited(cls, node_type: str) -> list:
        """!@Brief Get node inherited type."""
        return cmds.nodeType(node_type, inherited=True, isTypeName=True)
    
    @classmethod
    def __type_is_dag(cls, node_type: str) -> bool:
        return "dagNode" in cls._inherited(node_type)
    
    @classmethod
    def create(cls, node_type: str, node_name: str,
                parent: OpenMaya.MObject = None) -> OpenMaya.MObject:
        """!@Brief Create node from type."""
        modifier = cls.__dag_modifier if cls.__type_is_dag(node_type) else cls.__dg_modifier

        func = modifier.createNode
        new_node = func(node_type, parent) if parent else func(node_type)
        modifier.renameNode(new_node, node_name)
        modifier.doIt()

        return cls(new_node)