# coding=ascii

from typing import Union

from maya import OpenMaya

from Nodes.logger import log


class _Instances(object):

    __cls_instances = []

    def __init__(self):
        self.__instances = {}
        self.__cls_instances.append(self)
        self.__callback_id = OpenMaya.MDGMessage.addNodeRemovedCallback(self.remove)

    def __del__(self):
        OpenMaya.MMessage.removeCallback(self.__callback_id)

    @property
    def instances(self) -> dict:
        return self.__instances

    @staticmethod
    def __get_handle(node: Union[OpenMaya.MObject, OpenMaya.MDagPath]):
        if isinstance(node, OpenMaya.MDagPath):
            node = node.node()
        return OpenMaya.MObjectHandle(node)

    @staticmethod
    def __is_valid(handle):
        return not handle.object().isNull() and handle.isValid() and handle.isAlive()

    @staticmethod
    def __get_hash(handle: OpenMaya.MObjectHandle) -> str:
        return "%x" % handle.hashCode()

    def get(self, node: Union[OpenMaya.MObject, OpenMaya.MDagPath]) -> object:
        handle = self.__get_handle(node)
        if self.__is_valid(handle):
            hx = self.__get_hash(handle)
            if hx in self.__instances:
                instance = self.__instances[hx]
                instance.force_update_object(node)
                return instance

    def add(self, node: Union[OpenMaya.MObject, OpenMaya.MDagPath], node_cls: object):
        handle = self.__get_handle(node)
        if self.__is_valid(handle):
            hx = self.__get_hash(handle)
            if hx not in self.__instances:
                self.__instances[hx] = node_cls
            else:
                log.debug('Node already in instances')

    def remove(self, node: Union[OpenMaya.MObject, OpenMaya.MDagPath], *args, **kwargs):
        handle = self.__get_handle(node)
        if self.__is_valid(handle):
            hx = self.__get_hash(handle)
            if hx in self.__instances:
                del self.__instances[hx]

    @classmethod
    def reset(cls, *args, **kwargs):
        for instance in cls.__cls_instances:
            instance.__instances = {}


OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kMayaExiting, _Instances.reset)
OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, _Instances.reset)
