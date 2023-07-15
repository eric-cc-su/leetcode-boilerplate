import argparse
import requests

from re import match as re_match

CSRFTOKEN_KEY = "csrftoken"

class LeetcodeRequester:
    def __init__(self, url: str) -> None:
        # HTTP/GraphQL 
        self._urlpattern = r"https://leetcode.com/problems/(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)/"
        self._apiurl = "https://leetcode.com/graphql/"
        
        self.url = url
        self.slug = re_match(self._urlpattern, self.url).group('slug')

        self.cookie_dict = {}
        self.api_headers = {}

        print("Requesting...")
        self.request_main()
        self.request_question_info()
      
        # Question data
        self.question_num = None
        self.question_title = None
        self.code_snippets = None
    
    def request_main(self) -> None:
        main_r = requests.get(self.url)
        if main_r.status_code != 200:
            raise ValueError(f"Main request got an unexpected response: ${main_r.status_code} - ${main_r.reason}")
    
        # print(f"csrftoken cookie: {main_r.cookies.get(CSRFTOKEN_KEY)}")
        self.cookie_dict[CSRFTOKEN_KEY] = main_r.cookies.get(CSRFTOKEN_KEY)
        self.api_headers[f"x-{CSRFTOKEN_KEY}"] = main_r.cookies.get(CSRFTOKEN_KEY)
    
    def _form_question_title_query(self) -> dict:
        return {
            "query": "\n    query questionTitle($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    title\n    titleSlug\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n  }\n}\n",
            "variables": {
                "titleSlug": self.slug
            },
            "operationName": "questionTitle"
        }

    def _form_question_title_snippets_query(self) -> dict:
        return {
            "query":"\n    query questionEditorData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    title\n    codeSnippets {\n      lang\n      langSlug\n      code\n    }\n    envInfo\n    enableRunCode\n  }\n}\n    ",
            "variables": {"titleSlug": self.slug},
            "operationName":"questionEditorData"
        }

    def request_question_info(self) -> None:
        qinfo_r = requests.post(self._apiurl,
                                 json=self._form_question_title_snippets_query(),
                                 cookies=self.cookie_dict,
                                 headers=self.api_headers)
        print("API: question info requested")
        if qinfo_r.status_code != 200:
            raise ValueError(f"Main request got an unexpected response: ${qinfo_r.status_code} - ${qinfo_r.reason}")

        _response = qinfo_r
        r_content = _response.json()
        # question data is contained in data -> question
        try:
            q_data = r_content["data"]["question"]
        except KeyError as e:
            print("Question data could not be retrieved or response was in unexpected form")
        
        self.question_num = q_data["questionFrontendId"]
        self.question_title = q_data["title"]
        self.code_snippets = {
            obj["langSlug"]: obj for obj in q_data["codeSnippets"]
        }

    
if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description="Requests a problem from Leetcode"
    )

    print("Copy and paste the Leetcode URL:")
    leetcode_url = input()
  
    try:
        requester = LeetcodeRequester(leetcode_url)
        # print("Page requested")
    except Exception as error:
        print(f'ERROR: {error}')