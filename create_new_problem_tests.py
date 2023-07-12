import os
import shutil

from create_new_problem import Problem
from unittest import TestCase, main as unittest_main

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


class ProblemTest(FileWriteTestCase):
    def testInit(self) -> None:
        problem = Problem(PROBLEM_STRING, METHOD_DEF)
        self.assertIsInstance(problem, Problem)
        self.assertIsNotNone(problem.problem_string)
        self.assertIsNotNone(problem.filename)

        self.assertEqual(problem.problem_string, PROBLEM_STRING)
        self.assertEqual(problem.filename, FILENAME)

        self.assertIsNotNone(problem.method_def)
        self.assertIsNotNone(problem.method_name)
        self.assertEqual(problem.method_def, METHOD_DEF)
        self.assertEqual(problem.method_name, "searchBST")

        self.assertTrue(problem.encase)
    
    def testWriteFile(self) -> None:
        problem = Problem(PROBLEM_STRING, METHOD_DEF)
        self.assertFalse(os.path.exists(problem.filepath))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        os.remove(problem.filepath)


class FilepathTest(FileWriteTestCase):
    def testCurrentDirectory(self) -> None:
        problem = Problem(PROBLEM_STRING, METHOD_DEF, directory=CURRENT_DIRECTORY)
        self.assertEqual(problem.filepath, os.path.abspath(FILENAME))

        self.assertFalse(os.path.exists(FILENAME))
        problem.write_file()
        self.assertTrue(os.path.exists(FILENAME))
        os.remove(problem.filepath)

    def testChildDirectory(self) -> None:
        problem = Problem(PROBLEM_STRING, METHOD_DEF, directory=CHILD_DIRECTORY)
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(CHILD_DIRECTORY), FILENAME))

        self.assertTrue(os.path.exists(CHILD_DIRECTORY))

        self.assertFalse(os.path.exists(problem.filepath))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        self.assertFalse(os.path.exists(FILENAME))
        os.remove(problem.filepath)

    def testParentDirectory(self) -> None:
        problem = Problem(PROBLEM_STRING, METHOD_DEF, directory=PARENT_DIRECTORY)
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(PARENT_DIRECTORY), FILENAME))

        self.assertFalse(os.path.exists(problem.filepath))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        self.assertFalse(os.path.exists(FILENAME))
        os.remove(problem.filepath)

    def testMissingSlash(self) -> None:
        # Tests whether a valid filepath is created in the event the directory name is provided without a trailing slash
        problem = Problem(PROBLEM_STRING, METHOD_DEF, directory=PARENT_DIRECTORY.strip("/"))
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(PARENT_DIRECTORY.strip("/")), FILENAME))

        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        os.remove(problem.filepath)
        
        problem = Problem(PROBLEM_STRING, METHOD_DEF, directory=CHILD_DIRECTORY.strip("/"))
        self.assertEqual(problem.filepath, os.path.join(os.path.abspath(CHILD_DIRECTORY.strip("/")), FILENAME))

        self.assertTrue(os.path.exists(CHILD_DIRECTORY))
        problem.write_file()
        self.assertTrue(os.path.exists(problem.filepath))
        os.remove(problem.filepath)


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
        

class MethodTest(TestCase):
    def _equals_global(self, given: str) -> None:
        """
        Tests whether the 'given' method definition equals the global METHOD_DEF
        """
        problem = Problem(PROBLEM_STRING, given)

        self.assertEqual(problem.method_def, METHOD_DEF)

    def _equals_given(self, given: str) -> None:
        """
        Tests whether the 'given' method definition equals itself
        """
        problem = Problem(PROBLEM_STRING, given)
        
        self.assertEqual(problem.method_def, given)

    def testLeadingSpaces(self) -> None:
        self._equals_global(f"    {METHOD_DEF}")

    def testNoTyping(self) -> None:
        self._equals_given("def helloWorld(self, arg1):")

    def testNoArgs(self) -> None:
        self._equals_given("def helloworld():")

    def testNoMethod(self) -> None:
        problem = Problem(PROBLEM_STRING, '')

        self.assertEqual(problem.method_def, '')

    def testTypingImports(self) -> None:
        # Tests whether a typing imports are properly extracted from the given method definition
        problem = Problem(PROBLEM_STRING, METHOD_DEF)
        self.assertEqual(len(problem.typing_imports), 1)
        self.assertIn("Optional", problem.typing_imports)

        problem = Problem(PROBLEM_STRING, "def reverseList(self, head: Optional[ListNode], stuff: List[int]) -> Optional[ListNode]:")
        self.assertEqual(len(problem.typing_imports), 2)
        self.assertIn("List", problem.typing_imports)
        self.assertIn("Optional", problem.typing_imports)


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

if __name__ == "__main__":
    unittest_main()