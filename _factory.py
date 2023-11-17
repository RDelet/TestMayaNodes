# coding=ascii

import copy
import six
from typing import Union

from maya import OpenMaya

from TestMayaNodes import _instances, utils
from TestMayaNodes.logger import log


_registered = dict()


def create(node: OpenMaya.MObject) -> object:
    instance = _instances.get(node)
    return instance if instance else _create(node)


def _create(node: Union[str, OpenMaya.MObject]) -> object:
    if isinstance(node, str):
        node = utils.get_object(node)

    api_type = _get_type(node)
    new_cls = _registered[api_type](node)
    _instances.add(node, new_cls)

    return new_cls


def _get_type(node: OpenMaya.MObject):
    api_type = node.apiType()
    if not is_registered(api_type):
        if node.hasFn(OpenMaya.MFn.kDagNode):
            api_type = OpenMaya.MFn.kDagNode
        else:
            api_type = OpenMaya.MFn.kDependencyNode
    
    return api_type


def register():
    def do_register(class_obj: six.class_types):
        if not isinstance(class_obj, six.class_types):
            raise RuntimeError("This decorator can be use only by a class !")
        _do_register(class_obj)
        return class_obj
    return do_register


def _do_register(class_obj: six.class_types):
    api_type = class_obj.kApiType
    if is_registered(api_type):
        log.debug(f"Class {class_obj.__name__} already registered.")
        return

    _registered[api_type] = class_obj
    log.debug(f"Class {class_obj.__name__} registered.")


def is_registered(api_type: int) -> bool:
    return api_type in _registered


def registered() -> dict:
    return copy.copy(_registered)
