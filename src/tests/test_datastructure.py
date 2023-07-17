import os

from create_new_problem import Problem
from unittest import TestCase

TEST_SLUG = "hello-world"
TEST_URL = f"https://leetcode.com/problems/{TEST_SLUG}/"


class DSParamTest(TestCase):
    def testInvalid(self) -> None:
        with self.assertRaises(ValueError):
            self.problem = Problem(TEST_URL, data_structure="structure")

    def testNone(self) -> None:
        self.problem = Problem(TEST_URL)
        self.assertIsNone(self.problem.data_structure)

        self.problem = Problem(TEST_URL, data_structure=None)
        self.assertIsNone(self.problem.data_structure)

        self.assertEqual(len(self.problem.typing_imports), 0)

    def testLinkedList(self) -> None:
        self.problem = Problem(TEST_URL, data_structure='linked_list')
        self.assertEqual(self.problem.data_structure, "linked_list")
        self.assertEqual(len(self.problem.typing_imports), 1)
        self.assertTrue("Optional" in self.problem.typing_imports)

    def testTree(self) -> None:
        self.problem = Problem(TEST_URL, data_structure='tree')
        self.assertEqual(self.problem.data_structure, "tree")
        self.assertEqual(len(self.problem.typing_imports), 1)
        self.assertTrue("Optional" in self.problem.typing_imports)
