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

class FilepathTest(FileWriteTestCase):
    def testCurrentDirectory(self) -> None:
        problem = Problem(LEETCODE_URL, filename=FILENAME, directory=CURRENT_DIRECTORY)
        self.assertEqual(problem.filepath, os.path.abspath(FILENAME))

        problem.problem_string = PROBLEM_STRING
        problem.class_and_method = METHOD_DEF

        self.assertFalse(os.path.exists(FILENAME))
        problem.write_file()
        self.assertTrue(os.path.exists(FILENAME))
        os.remove(problem.filepath)

    def testChildDirectory(self) -> None:
        problem = Problem(LEETCODE_URL, filename=FILENAME, directory=CHILD_DIRECTORY)
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(CHILD_DIRECTORY), FILENAME))

        self.assertTrue(os.path.exists(CHILD_DIRECTORY))

        problem.problem_string = PROBLEM_STRING
        problem.class_and_method = METHOD_DEF

        self.assertFalse(os.path.exists(problem.filepath))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        self.assertFalse(os.path.exists(FILENAME))
        os.remove(problem.filepath)

    def testParentDirectory(self) -> None:
        problem = Problem(LEETCODE_URL, filename=FILENAME, directory=PARENT_DIRECTORY)
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(PARENT_DIRECTORY), FILENAME))

        problem.problem_string = PROBLEM_STRING
        problem.class_and_method = METHOD_DEF

        self.assertFalse(os.path.exists(problem.filepath))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        self.assertFalse(os.path.exists(FILENAME))
        os.remove(problem.filepath)

    def testMissingSlash(self) -> None:
        # Tests whether a valid filepath is created in the event the directory name is provided without a trailing slash
        problem = Problem(LEETCODE_URL, filename=FILENAME, directory=PARENT_DIRECTORY.strip("/"))
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(PARENT_DIRECTORY.strip("/")), FILENAME))

        problem.problem_string = PROBLEM_STRING
        problem.class_and_method = METHOD_DEF

        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        os.remove(problem.filepath)
        
        problem = Problem(LEETCODE_URL, filename=FILENAME, directory=CHILD_DIRECTORY.strip("/"))
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(CHILD_DIRECTORY.strip("/")), FILENAME))

        problem.problem_string = PROBLEM_STRING
        problem.class_and_method = METHOD_DEF

        self.assertTrue(os.path.exists(CHILD_DIRECTORY))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        os.remove(problem.filepath)