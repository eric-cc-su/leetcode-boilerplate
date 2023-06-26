import os

from create_new_problem import Problem
from unittest import TestCase, main as unittest_main

PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = ""
CHILD_DIRECTORY = "child/"
PARENT_DIRECTORY = "../"


class ProblemTest(TestCase):
    def testInit(self) -> None:
        problem = Problem(CURRENT_DIRECTORY, PROBLEM_STRING, METHOD_DEF)
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


class FilepathTest(TestCase):
    def testCurrentDirectory(self) -> None:
        problem = Problem(CURRENT_DIRECTORY, PROBLEM_STRING, METHOD_DEF)

        self.assertEqual(problem.filepath, FILENAME)

    def testChildDirectory(self) -> None:
        problem = Problem(CHILD_DIRECTORY, PROBLEM_STRING, METHOD_DEF)

        self.assertEqual(problem.filepath, os.path.join(CHILD_DIRECTORY, FILENAME))

    def testParentDirectory(self) -> None:
        problem = Problem(PARENT_DIRECTORY, PROBLEM_STRING, METHOD_DEF)

        self.assertEqual(problem.filepath, os.path.join(PARENT_DIRECTORY, FILENAME))

    def testMissingSlash(self) -> None:
        # Tests whether a valid filepath is created in the event the directory name is provided without a trailing slash
        problem = Problem("..", PROBLEM_STRING, METHOD_DEF)
        self.assertEqual(problem.filepath, os.path.join("..", FILENAME))

        problem = Problem("child", PROBLEM_STRING, METHOD_DEF)
        self.assertEqual(problem.filepath, os.path.join("child", FILENAME))


class FilenameTest(TestCase):
    def testMultipleSpaces(self) -> None:
        problem_string = "532. There are  multiple   spaces"
        problem = Problem(CURRENT_DIRECTORY, problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "532. There are multiple spaces")
        self.assertEqual(problem.filename, "p532-there_are_multiple_spaces.py")
    
    def testNoProblemNum(self) -> None:
        problem_string = ". hello world"
        with self.assertRaises(Exception):
            Problem(CURRENT_DIRECTORY, problem_string, METHOD_DEF)

    def testNoPeriod(self) -> None:
        problem_string = "123 hello world"
        problem = Problem(CURRENT_DIRECTORY, problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, FILENAME)
    
    def testNoPeriodSpace(self) -> None:
        problem_string = "123.hello world"
        problem = Problem(CURRENT_DIRECTORY, problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, FILENAME)

    def testMissingOptionals(self) -> None:
        problem_string = "123hello world"
        problem = Problem(CURRENT_DIRECTORY, problem_string, METHOD_DEF)
    
        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, FILENAME)
        

class MethodTest(TestCase):
    def _equals_global(self, given: str) -> None:
        """
        Tests whether the 'given' method definition equals the global METHOD_DEF
        """
        problem = Problem(CURRENT_DIRECTORY, PROBLEM_STRING, given)

        self.assertEqual(problem.method_def, METHOD_DEF)

    def _equals_given(self, given: str) -> None:
        """
        Tests whether the 'given' method definition equals itself
        """
        problem = Problem(CURRENT_DIRECTORY, PROBLEM_STRING, given)
        
        self.assertEqual(problem.method_def, given)

    def testLeadingSpaces(self) -> None:
        self._equals_global(f"    {METHOD_DEF}")

    def testNoTyping(self) -> None:
        self._equals_given("def helloWorld(self, arg1):")

    def testNoArgs(self) -> None:
        self._equals_given("def helloworld():")

    def testNoMethod(self) -> None:
        problem = Problem(CURRENT_DIRECTORY, PROBLEM_STRING, '')

        self.assertEqual(problem.method_def, '')

if __name__ == "__main__":
    unittest_main()