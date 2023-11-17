# coding=ascii

from typing import Union

from maya.api import OpenMaya

from TestMayaNodes import utils


_instances = {}


def get(node: Union[OpenMaya.MObject, OpenMaya.MDagPath]) -> object:
    handle = utils.get_handle(node)
    if utils.is_valid(handle):
        hx = utils.get_hash(handle)
        if hx in _instances:
            instance = _instances[hx]
            instance._object(node)
            return instance


def add(node: Union[OpenMaya.MObject, OpenMaya.MDagPath], node_cls: object):
    handle = utils.get_handle(node)
    if utils.is_valid(handle):
        hx = utils.get_hash(handle)
        if hx not in _instances:
            _instances[hx] = node_cls


def remove(node: Union[OpenMaya.MObject, OpenMaya.MDagPath], *args, **kwargs):
    handle = utils.get_handle(node)
    if utils.is_valid(handle):
        hx = utils.get_hash(handle)
        if hx in _instances:
            del _instances[hx]
        


def _clear(*args, **kwargs):
    _instances = {}


OpenMaya.MDGMessage.addNodeRemovedCallback(remove, "node")  # node = all maya nodes
OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kMayaExiting, _clear)
OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, _clear)
