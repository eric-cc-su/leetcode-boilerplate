import os
import shutil

from unittest import TestCase

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"
PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = "./"
CHILD_DIRECTORY = "test-child/"
PARENT_DIRECTORY = "../"

class FileWriteTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Set up empty test child directory before running all tests
        if not os.path.exists(CHILD_DIRECTORY):
            os.makedirs(CHILD_DIRECTORY)
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        # Delete the entire test child directory after test suite
        if os.path.exists(CHILD_DIRECTORY):
            shutil.rmtree(CHILD_DIRECTORY)
        return super().tearDownClass()
    
    def tearDown(self) -> None:
        # Delete any straggler test files after a test
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
        if os.path.exists(os.path.join(CHILD_DIRECTORY, FILENAME)):
            os.remove(os.path.join(CHILD_DIRECTORY, FILENAME))
        if os.path.exists(os.path.join(PARENT_DIRECTORY, FILENAME)):
            os.remove(os.path.join(PARENT_DIRECTORY), FILENAME)
        
        return super().tearDown()