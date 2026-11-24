import inspect
import re
import typing

import pytest

from tapi import Tines
from tests.support import is_sequence, public_methods


@pytest.fixture
def methods(tines):
    return public_methods(tines=tines)


def test_every_method_and_constructor_takes_keyword_only_arguments(tines, methods):
    classes = {type(method.__self__) for method in methods.values()}
    functions = dict(methods)
    functions.update({f"{cls.__name__}.__init__": cls.__init__ for cls in classes})
    functions["Tines.__init__"] = Tines.__init__

    offenders = [
        name
        for name, function in functions.items()
        for parameter in list(inspect.signature(function).parameters.values())[
            1 if name.endswith("__init__") else 0 :
        ]
        if parameter.kind is not inspect.Parameter.KEYWORD_ONLY
    ]

    assert offenders == []


def test_every_method_documents_its_arguments_and_its_reply(methods):
    problems = []
    for name, method in methods.items():
        doc = inspect.getdoc(method) or ""
        arguments = doc.split("Args:")[1].split("Returns:")[0] if "Args:" in doc else ""
        problems += [
            f"{name}: no description of {parameter}"
            for parameter in inspect.signature(method).parameters
            if not re.search(rf"^\s*{parameter}:", arguments, re.MULTILINE)
        ]
        if "Returns:" not in doc:
            problems.append(f"{name}: no Returns section")

    assert problems == []


def test_a_single_string_is_rejected_for_every_sequence_argument(tines, router, methods):
    accepted = []
    for name, method in methods.items():
        hints = typing.get_type_hints(method)
        required = {
            parameter.name: [1] if is_sequence(hint=hints[parameter.name]) else 1
            for parameter in inspect.signature(method).parameters.values()
            if parameter.default is inspect.Parameter.empty
        }
        for parameter in inspect.signature(method).parameters:
            if not is_sequence(hint=hints[parameter]):
                continue
            try:
                method(**{**required, parameter: "abc"})
            except TypeError:
                continue
            accepted.append(f"{name}: {parameter}")

    assert accepted == []
