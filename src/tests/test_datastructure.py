from create_new_problem import Problem
from unittest import TestCase, main as unittest_main

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"
PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = "./"
CHILD_DIRECTORY = "test-child/"
PARENT_DIRECTORY = "../"

class DataStructureTest(TestCase):
    def testInvalid(self) -> None:
        with self.assertRaises(ValueError):
            self.problem = Problem(PROBLEM_STRING, METHOD_DEF, data_structure="structure")

    def testNone(self) -> None:
        self.problem = Problem(PROBLEM_STRING, METHOD_DEF)
        self.assertIsNone(self.problem.data_structure)

        self.problem = Problem(PROBLEM_STRING, METHOD_DEF, data_structure=None)
        self.assertIsNone(self.problem.data_structure)

    def testLinkedList(self) -> None:
        self.problem = Problem(PROBLEM_STRING, METHOD_DEF, data_structure='linked_list')
        self.assertEqual(self.problem.data_structure, "linked_list")

    def testTree(self) -> None:
        self.problem = Problem(PROBLEM_STRING, METHOD_DEF, data_structure='tree')
        self.assertEqual(self.problem.data_structure, "tree")