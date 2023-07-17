import os
import responses
from create_new_problem import Problem
from requests import ConnectTimeout, ReadTimeout
from unittest import TestCase
from LeetcodeRequester import LeetcodeRequester
from src.tests.FileWriteTestCase import FileWriteTestCase

CSRFTOKEN_KEY = "csrftoken"
CSRFTOKEN_DUMMY = "123abc"
TEST_SLUG = "test-problem"
TEST_QUESTION_NUM = "123"
TEST_QUESTION_TITLE = TEST_SLUG.replace("-", " ").capitalize()
LEETCODE_TEST_URL = f"https://leetcode.com/problems/{TEST_SLUG}/"
LEETCODE_TEST_URL_EXT = f"https://leetcode.com/problems/{TEST_SLUG}/?envType=study-plan-v2&envId=leetcode-75"
LEETCODE_API_TEST_URL = "https://leetcode.com/graphql/"

EDITOR_REQUEST_QUERY = {
    "query":"\n    query questionEditorData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    title\n    codeSnippets {\n      lang\n      langSlug\n      code\n    }\n    envInfo\n    enableRunCode\n  }\n}\n    ",
    "variables": {"titleSlug": TEST_SLUG},
    "operationName":"questionEditorData"
}
EDITOR_RESPONSE_DATA = {
    "data": {
        "question": {
            "questionId": TEST_QUESTION_NUM,
            "questionFrontendId": TEST_QUESTION_NUM,
            "title": TEST_QUESTION_TITLE,
            "codeSnippets": [
                {
                    "lang": "Python",
                    "langSlug": "python",
                    "code": "class Solution(object):\n    def testMethod(self, s):\n        \"\"\"\n        :type s: str\n        :rtype: str\n        \"\"\"\n        "
                },
                {
                    "lang": "Python3",
                    "langSlug": "python3",
                    "code": "class Solution:\n    def testMethod(self, s: str) -> str:\n        "
                }
            ],
            "envInfo": "{...}",
            "enableRunCode": True
        }
    }
}


class RequesterTest(TestCase):
    def setUp(self) -> None:
        self.requester = LeetcodeRequester(LEETCODE_TEST_URL)
        return super().setUp()

    def testInit(self) -> None:
        self.assertIsInstance(self.requester.request_timeout, int)
        self.assertIsInstance(self.requester.max_retries, int)
        self.assertFalse(self.requester.abort_all)

        self.assertIsInstance(self.requester.url, str)
        self.assertEqual(self.requester.url, LEETCODE_TEST_URL)
        self.assertIsInstance(self.requester.slug, str)
        self.assertEqual(self.requester.slug, TEST_SLUG)

        self.assertIsInstance(self.requester.cookie_dict, dict)
        self.assertIsInstance(self.requester.api_headers, dict)
        self.assertEqual(len(self.requester.cookie_dict), 0)
        self.assertEqual(len(self.requester.api_headers), 0)

        self.assertIsNone(self.requester.question_num)
        self.assertIsNone(self.requester.question_title)
        self.assertIsNone(self.requester.code_snippets)

    def testSetSlug(self) -> None:
        self.assertIsInstance(self.requester.url, str)
        self.assertEqual(self.requester.url, LEETCODE_TEST_URL)
        self.assertIsInstance(self.requester.slug, str)
        self.assertEqual(self.requester.slug, TEST_SLUG)

        self.requester.setUrl(LEETCODE_TEST_URL.strip("/"))
        self.assertIsInstance(self.requester.url, str)
        self.assertEqual(self.requester.url, LEETCODE_TEST_URL.strip("/"))
        self.assertIsInstance(self.requester.slug, str)
        self.assertEqual(self.requester.slug, TEST_SLUG)

        self.requester.setUrl(LEETCODE_TEST_URL_EXT)
        self.assertIsInstance(self.requester.url, str)
        self.assertEqual(self.requester.url, LEETCODE_TEST_URL_EXT)
        self.assertIsInstance(self.requester.slug, str)
        self.assertEqual(self.requester.slug, TEST_SLUG)
    
    @responses.activate
    def testMainConnectTimeout(self) -> None:
        """ Tests a simulated connection timeout for the GET request to Leetcode """
        responses.get(
            LEETCODE_TEST_URL,
            body=ConnectTimeout()
        )
        self.requester._request_main()
        self.assertTrue(self.requester.abort_all)
        self.assertEqual(len(self.requester.cookie_dict), 0)
        self.assertEqual(len(self.requester.api_headers), 0)

        self.assertIsNone(self.requester.question_num)
        self.assertIsNone(self.requester.question_title)
        self.assertIsNone(self.requester.code_snippets)
    
    @responses.activate
    def testMainReadTimeout(self) -> None:
        """ Tests a simulated read timeout for the GET request to Leetcode """
        responses.get(
            LEETCODE_TEST_URL,
            body=ReadTimeout()
        )
        self.requester._request_main()
        self.assertTrue(self.requester.abort_all)
        self.assertEqual(len(self.requester.cookie_dict), 0)
        self.assertEqual(len(self.requester.api_headers), 0)

        self.assertIsNone(self.requester.question_num)
        self.assertIsNone(self.requester.question_title)
        self.assertIsNone(self.requester.code_snippets)
    
    @responses.activate
    def testAPIConnectTimeout(self) -> None:
        responses.post(
            self.requester._apiurl,
            body=ConnectTimeout()
        )
        self.requester._request_question_info()
        self.assertTrue(self.requester.abort_all)
        self.assertIsNone(self.requester.question_num)
        self.assertIsNone(self.requester.question_title)
        self.assertIsNone(self.requester.code_snippets)
    
    @responses.activate
    def testAPIReadTimeout(self) -> None:
        responses.post(
            self.requester._apiurl,
            body=ReadTimeout()
        )
        self.requester._request_question_info()
        self.assertTrue(self.requester.abort_all)
        self.assertIsNone(self.requester.question_num)
        self.assertIsNone(self.requester.question_title)
        self.assertIsNone(self.requester.code_snippets)


class DataTest(TestCase):
    def setUp(self) -> None:
        self.requester = LeetcodeRequester(LEETCODE_TEST_URL)
        return super().setUp()

    @responses.activate
    def testMain(self) -> None:
        responses.get(
            LEETCODE_TEST_URL,
            headers={"Set-Cookie": f"{CSRFTOKEN_KEY}:{CSRFTOKEN_DUMMY}"}
        )

        self.requester._request_main()
        self.assertFalse(self.requester.abort_all)

        self.assertEqual(len(self.requester.cookie_dict), 1)
        self.assertEqual(len(self.requester.api_headers), 1)
        self.assertIn(CSRFTOKEN_KEY, self.requester.cookie_dict)
        self.assertIn(f"x-{CSRFTOKEN_KEY}", self.requester.api_headers)

    @responses.activate
    def testApi(self) -> None:
        responses.post(
            LEETCODE_API_TEST_URL,
            match=[
                responses.matchers.json_params_matcher(EDITOR_REQUEST_QUERY)
            ],
            json=EDITOR_RESPONSE_DATA
        )
        self.requester._request_question_info()
        self.assertEqual(self.requester.question_num, TEST_QUESTION_NUM)
        self.assertEqual(self.requester.question_title, TEST_QUESTION_TITLE)
        self.assertIsInstance(self.requester.code_snippets, dict)
        self.assertIn("python3", self.requester.code_snippets)
    

class ProblemRequestTest(FileWriteTestCase):
    @classmethod
    @responses.activate
    def setUpClass(cls) -> None:
        responses.get(
            LEETCODE_TEST_URL,
            headers={"Set-Cookie": f"{CSRFTOKEN_KEY}:{CSRFTOKEN_DUMMY}"}
        )
        responses.post(
            LEETCODE_API_TEST_URL,
            match=[
                responses.matchers.json_params_matcher(EDITOR_REQUEST_QUERY)
            ],
            json=EDITOR_RESPONSE_DATA
        )
        # Set up shared problem class to request only one problem
        cls.problem = Problem(LEETCODE_TEST_URL)

        cls.problem.request()

        return super().setUpClass()

    def testRequest(self) -> None:
        # Allow for timeout failures
        self.assertIsNotNone(self.problem.problem_string)
        self.assertEqual(self.problem.problem_string, f"{TEST_QUESTION_NUM}. {TEST_QUESTION_TITLE}")
        self.assertIsNotNone(self.problem.filename)
        self.assertEqual(self.problem.filename, f"p{TEST_QUESTION_NUM}-{TEST_SLUG}.py")
        self.assertIsNotNone(self.problem.filepath)
        self.assertEqual(self.problem.filepath, os.path.abspath(f"./p{TEST_QUESTION_NUM}-{TEST_SLUG}.py"))

    def testWriteFile(self) -> None:
        self.problem.write_file()
        self.assertTrue(os.path.exists(self.problem.filepath))
        os.remove(self.problem.filepath)