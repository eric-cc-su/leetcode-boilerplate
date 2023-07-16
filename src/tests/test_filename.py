from create_new_problem import Problem
from unittest import TestCase, main as unittest_main

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"
PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = "./"
CHILD_DIRECTORY = "test-child/"
PARENT_DIRECTORY = "../"


class FilenameTest(TestCase):
    def testMultipleSpaces(self) -> None:
        problem_string = "532. There are  multiple   spaces"
        problem = Problem(problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "532. There are multiple spaces")
        self.assertEqual(problem.filename, "p532-there_are_multiple_spaces.py")
    
    def testNoProblemNum(self) -> None:
        problem_string = ". hello world"
        with self.assertRaises(Exception):
            Problem(problem_string, METHOD_DEF)

    def testNoPeriod(self) -> None:
        problem_string = "123 hello world"
        problem = Problem(problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, FILENAME)
    
    def testNoPeriodSpace(self) -> None:
        problem_string = "123.hello world"
        problem = Problem(problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, FILENAME)

    def testMissingOptionals(self) -> None:
        problem_string = "123hello world"
        problem = Problem(problem_string, METHOD_DEF)
    
        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, FILENAME)