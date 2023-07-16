import os

from create_new_problem import Problem
from src.tests.FileWriteTestCase import FileWriteTestCase

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"
PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = "./"
CHILD_DIRECTORY = "test-child/"
PARENT_DIRECTORY = "../"

class ProblemTest(FileWriteTestCase):
    def setUp(self) -> None:
        self.problem = Problem(LEETCODE_URL)
        return super().setUp()

    def testInit(self) -> None:
        self.assertIsInstance(self.problem, Problem)
        self.assertIsNone(self.problem.problem_string)
        self.assertIsNotNone(self.problem.directory)
        self.assertIsNone(self.problem.filename)
        self.assertIsNone(self.problem.filepath)
        self.assertEqual(self.problem.classname, "Solution")
        self.assertIsNone(self.problem.method_name)
        self.assertIsNone(self.problem.class_and_method)
        self.assertIsNone(self.problem.data_structure)
        self.assertIsInstance(self.problem.typing_imports, set)
        self.assertEqual(len(self.problem.typing_imports), 0)

class ProblemRequestedTest(FileWriteTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Set up shared problem class to request only one problem
        cls.problem = Problem(LEETCODE_URL)

        for i in range(3):
            cls.problem.request()
            if cls.problem.filepath:
                break

        return super().setUpClass()

    def testRequest(self) -> None:
        # Allow for timeout failures
        self.assertIsNotNone(self.problem.problem_string)
        self.assertEqual(self.problem.problem_string, "1004. Max Consecutive Ones III")
        self.assertIsNotNone(self.problem.filename)
        self.assertEqual(self.problem.filename, "p1004-max-consecutive-ones-iii.py")
        self.assertIsNotNone(self.problem.filepath)
        self.assertEqual(self.problem.filepath, os.path.abspath("./p1004-max-consecutive-ones-iii.py"))

    def testWriteFile(self) -> None:
        self.problem.write_file()
        self.assertTrue(os.path.exists(self.problem.filepath))
        os.remove(self.problem.filepath)