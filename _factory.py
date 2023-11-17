# coding=ascii

import copy
import six

from maya import OpenMaya

from Nodes._instances import _Instances
from Nodes.logger import log


class _Factory(object):

    __registered_cls = dict()
    __instances = _Instances()

    @classmethod
    def create(cls, node: OpenMaya.MObject) -> object:
        instance = cls.__instances.get(node)
        return instance if instance else cls._create(node)

    @classmethod
    def _create(cls, node: OpenMaya.MObject) -> object:
        api_type = node.apiType()
        if not _Factory.is_registered(api_type):
            if node.hasFn(OpenMaya.MFn.kDagNode):
                api_type = OpenMaya.MFn.kDagNode
            else:
                api_type = OpenMaya.MFn.kDependencyNode

        new_instances = cls.__registered_cls[api_type](node)
        cls.__instances.add(node, new_instances)

        return new_instances

    @classmethod
    def _do_register(cls, class_obj: six.class_types):
        if not isinstance(class_obj, six.class_types):
            raise RuntimeError("Only class can be registered !")

        api_type = class_obj.kApiType
        if api_type in cls.__registered_cls:
            raise ValueError(f"Object {class_obj.__name__} has already been registered !")

        cls.__registered_cls[api_type] = class_obj
        log.debug(f"Class {class_obj.__name__} registered.")

    @classmethod
    def is_registered(cls, api_type: int) -> bool:
        return api_type in cls.__registered_cls

    @classmethod
    def register(cls):
        def do_register(class_obj: six.class_types):
            if not isinstance(class_obj, six.class_types):
                raise RuntimeError("This decorator can be use only by a class !")
            cls._do_register(class_obj)
            return class_obj
        return do_register

    @classmethod
    def registered(cls) -> dict:
        return copy.copy(cls.__registered_cls)
