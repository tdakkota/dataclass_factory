#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from enum import Enum
from typing import List, Dict, Optional, Any

from dataclasses import field, dataclass

from dataclass_factory import Factory


class State(Enum):
    one = "1"
    two = "two"


@dataclass
class D:
    a: int
    b: int = field(init=False, default=1)
    c: str = "def_value"


@dataclass
class ListD:
    data: List[D]
    ints: List[int]


@dataclass
class DictD:
    data: Dict[str, D]
    strs: Dict[str, str]


class TestSerializer(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = Factory()

    def test_plain(self):
        serializer = self.factory.serializer(D)
        d = D(100, "hello")
        self.assertEqual(
            serializer(d),
            {"a": 100, "b": 1, "c": "hello"},
        )

    def test_list(self):
        serializer = self.factory.serializer(ListD)
        d1 = D(100, "hello")
        d2 = D(200, "hello2")

        dlist = ListD(
            [d1, d2],
            [123, 456, 789],
        )
        data = {
            "data": [
                {"a": 100, "b": 1, "c": "hello"},
                {"a": 200, "b": 1, "c": "hello2"},
            ],
            "ints": [123, 456, 789],
        }
        self.assertEqual(
            serializer(dlist),
            data,
        )

    def test_dict(self):
        serializer = self.factory.serializer(DictD)
        d1 = D(100, "hello")
        d2 = D(200, "hello2")

        dlist = DictD(
            {"1": d1, "two": d2},
            {"hello": "world", "foo": "bar"}
        )
        data = {
            "data": {
                "1": {"a": 100, "b": 1, "c": "hello"},
                "two": {"a": 200, "b": 1, "c": "hello2"},
            },
            "strs": {"hello": "world", "foo": "bar"}
        }
        self.assertEqual(
            serializer(dlist),
            data,
        )

    def test_optional(self):
        serializer = self.factory.serializer(Optional[D])
        d1 = D(100, "hello")
        data1 = {"a": 100, "b": 1, "c": "hello"}
        self.assertEqual(
            serializer(d1),
            data1,
        )
        self.assertIs(
            serializer(None),
            None,
        )

    def test_any(self):
        serializer = self.factory.serializer(Any)
        d1 = D(100, "hello")
        data1 = {"a": 100, "b": 1, "c": "hello"}
        self.assertEqual(
            serializer(d1),
            data1,
        )
        self.assertIs(
            serializer(None),
            None,
        )

    def test_enum(self):
        self.assertEqual(self.factory.dump(State.one), "1")
        self.assertEqual(self.factory.dump(State.two, State), "two")
