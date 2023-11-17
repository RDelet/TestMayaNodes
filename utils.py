from typing import Union

from maya import cmds
from maya.api import OpenMaya


_dagMod = OpenMaya.MDagModifier()
_dgMod = OpenMaya.MDGModifier()
_msl = OpenMaya.MSelectionList()
_nullObj = OpenMaya.MObject.kNullObj

kDagNodeType = cmds.nodeType('dagNode', derived=True, isTypeName=True)



def get_object(node: str) -> OpenMaya.MObject:
    """!@Brief Get MObject of current node."""

    try:
        _msl.clear()
        _msl.add(node)
        return _msl.getDependNode(0)
    except RuntimeError:
        raise RuntimeError(f"Node {node} does not exist !")


def get_path(node: Union[str, OpenMaya.MObject]) -> OpenMaya.MDagPath:
    if isinstance(node, OpenMaya.MObject):
        if not node.hasFn(OpenMaya.MFn.kDagNode):
            raise RuntimeError(f"Node {name(node)} is not a dagNode !")
        return OpenMaya.MDagPath.getAPathTo(node)
    
    try:
        _msl.clear()
        _msl.add(node)
        return _msl.getDagPath(0)
    except RuntimeError:
        raise RuntimeError(f"Node {node} does not exist !")


def check_object(obj: Union[str, OpenMaya.MObject]) -> OpenMaya.MObject:
    if isinstance(obj, str):
        obj = get_object(obj)
    elif isinstance(obj, OpenMaya.MObject) and not is_valid(obj):
        raise RuntimeError("Invalid MObject !")
    return obj


def get_handle(node: OpenMaya.MObject) -> OpenMaya.MObjectHandle:
    return OpenMaya.MObjectHandle(node)


def is_valid(obj: Union[OpenMaya.MObject, OpenMaya.MObjectHandle]) -> bool:
    if isinstance(obj, OpenMaya.MObject):
        node = obj
        handle = get_handle(obj)
    else:
        handle = obj
        node = handle.object()
        
    return not node.isNull() and handle.isValid() and handle.isAlive()


def get_hash(obj: Union[OpenMaya.MObject, OpenMaya.MObjectHandle]) -> str:
    if isinstance(obj, OpenMaya.MObject):
        obj = get_handle(obj)
    return "%x" % obj.hashCode()


def name(obj: Union[OpenMaya.MObject, OpenMaya.MDagPath, OpenMaya.MPlug],
         full: bool = True, namespace: bool = True) -> str:
    if isinstance(obj, OpenMaya.MDagPath):
        name = obj.fullPathName()
    elif isinstance(obj, OpenMaya.MPlug):
        node_name = name(obj.node())
        attr_name = OpenMaya.MFnAttribute(obj.attribute()).name()
        name = f"{node_name}.{attr_name}"
    if isinstance(obj, OpenMaya.MObject):
        if not obj.hasFn(OpenMaya.MFn.kDagNode):
            name = OpenMaya.MFnDependencyNode(obj).name()
        else:
            name = OpenMaya.MFnDagNode(obj).fullPathName()
    else:
        raise TypeError(f"Argument must be a MObject not {type(obj)}")
    
    if not full:
        name = name.split('|')[-1]
    if not namespace:
        name = name.split(':')[-1]
    
    return name


def create(node_type: str, name: str = None, restriction: int = 0,
           parent: Union[str, OpenMaya.MObject] = _nullObj) -> OpenMaya.MObject:

    is_dag = node_type in kDagNodeType
    modifier = _dagMod if is_dag else _dgMod

    if node_type == "objectSet":
        new_node = OpenMaya.MFnSet().create(OpenMaya.MSelectionList(), restriction)
    else:
        if isinstance(parent, str):
            parent = get_object(parent)
        new_node = modifier.createNode(node_type, parent)

    modifier.renameNode(new_node, name if name else f"{node_type}1")
    modifier.doIt()

    return new_node
