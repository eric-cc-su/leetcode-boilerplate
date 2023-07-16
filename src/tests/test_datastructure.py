import os

from create_new_problem import Problem
from unittest import TestCase, main as unittest_main
from src.tests.FileWriteTestCase import FileWriteTestCase

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"
PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = "./"


class DSParamTest(TestCase):
    def testInvalid(self) -> None:
        with self.assertRaises(ValueError):
            self.problem = Problem(LEETCODE_URL, data_structure="structure")

    def testNone(self) -> None:
        self.problem = Problem(LEETCODE_URL)
        self.assertIsNone(self.problem.data_structure)

        self.problem = Problem(LEETCODE_URL, data_structure=None)
        self.assertIsNone(self.problem.data_structure)

        self.assertEqual(len(self.problem.typing_imports), 0)

    def testLinkedList(self) -> None:
        self.problem = Problem(LEETCODE_URL, data_structure='linked_list')
        self.assertEqual(self.problem.data_structure, "linked_list")
        self.assertEqual(len(self.problem.typing_imports), 1)
        self.assertTrue("Optional" in self.problem.typing_imports)

    def testTree(self) -> None:
        self.problem = Problem(LEETCODE_URL, data_structure='tree')
        self.assertEqual(self.problem.data_structure, "tree")
        self.assertEqual(len(self.problem.typing_imports), 1)
        self.assertTrue("Optional" in self.problem.typing_imports)
