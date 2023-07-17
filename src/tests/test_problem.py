from create_new_problem import Problem
from src.tests.FileWriteTestCase import FileWriteTestCase

LEETCODE_URL = "https://leetcode.com/problems/max-consecutive-ones-iii/?envType=study-plan-v2&envId=leetcode-75"


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
    
    def testNoRequesterInfo(self) -> None:
        self.assertIsNone(self.problem._requester.question_num)
        self.assertIsNone(self.problem._requester.question_title)
        self.assertIsNone(self.problem._requester.code_snippets)

        with self.assertRaises(AttributeError):
            self.problem._assemble_problem_string_and_filename()
        
        with self.assertRaises(AttributeError):
            self.problem._assemble_code()