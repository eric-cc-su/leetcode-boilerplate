from create_new_problem import Problem
from unittest import TestCase, main as unittest_main

PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"


class ProblemTest(TestCase):
    def testInit(self) -> None:
        problem = Problem(PROBLEM_STRING, METHOD_DEF)
        self.assertIsInstance(problem, Problem)
        self.assertIsNotNone(problem.problem_string)
        self.assertIsNotNone(problem.filename)

        self.assertEqual(problem.problem_string, PROBLEM_STRING)
        self.assertEqual(problem.filename, "p123-hello_world.py")

        self.assertIsNotNone(problem.method_def)
        self.assertIsNotNone(problem.method_name)
        self.assertEqual(problem.method_def, METHOD_DEF)
        self.assertEqual(problem.method_name, "searchBST")

        self.assertTrue(problem.encase)


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
        self.assertEqual(problem.filename, "p123-hello_world.py")
    
    def testNoPeriodSpace(self) -> None:
        problem_string = "123.hello world"
        problem = Problem(problem_string, METHOD_DEF)

        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, "p123-hello_world.py")

    def testMissingOptionals(self) -> None:
        problem_string = "123hello world"
        problem = Problem(problem_string, METHOD_DEF)
    
        self.assertEqual(problem.problem_string, "123. hello world")
        self.assertEqual(problem.filename, "p123-hello_world.py")
        

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

if __name__ == "__main__":
    unittest_main()