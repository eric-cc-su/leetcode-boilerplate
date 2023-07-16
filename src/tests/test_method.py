from create_new_problem import Problem
from unittest import TestCase, main as unittest_main

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"
PROBLEM_STRING = "123. Hello World"
METHOD_DEF = "def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:"
FILENAME = "p123-hello_world.py"
CURRENT_DIRECTORY = "./"
CHILD_DIRECTORY = "test-child/"
PARENT_DIRECTORY = "../"

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
