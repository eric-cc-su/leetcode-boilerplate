# A script to create the boilerplate for a new Leetcode problem that comes with unit testing 
#
# Python 3.6+ required
#
# Inputs:
# - The Leetcode URL
# Optional:
# - directory
# - file name
# - data structure
import argparse
import os

from re import findall, search as re_search
from sys import argv
from typing import Optional

from LeetcodeRequester import LeetcodeRequester

# Constant for how to indent (currently using one tab equals four spaces)
INDENT = "    "

DATA_STRUCTURE_IMPORTS = {
    'linked_list': 'from leetcode_linkedlist import LinkedList, ListNode\n',
    'tree': 'from leetcode_treenode import Tree, TreeNode\n',
}

DATA_STRUCTURE_TEST = {
    'linked_list': 'self.ll = LinkedList()',
    'tree': 'self.tree = Tree()'
}


class Problem:
    def __init__(self, url: str,
                 directory: Optional[str]=".",
                 data_structure: Optional[str]=None, filename: Optional[str]=None) -> None:
        # Initiate requester
        self._requester = LeetcodeRequester(url)

        # Handle problem string
        self.problem_string = None

        self.directory = directory
        self.filename = filename
        self.filepath = None

        if self.filename:
            self.filepath = os.path.join(os.path.abspath(self.directory), self.filename)
            # Check if a file already exists with the same name
            if os.path.exists(self.filepath):
                raise FileExistsError
        
        self.typing_imports = set()
        # Handle data structure
        # Needs to be done before handling method definition to avoid overwriting typing_imports
        if data_structure:
            if data_structure not in DATA_STRUCTURE_IMPORTS.keys():
                raise ValueError(f"Data structure {data_structure} not supported")
            else:
                self.typing_imports.add("Optional")
        self.data_structure = data_structure

        # Handle method definition, including typing_imports parsing
        self.classname = "Solution"
        self.method_name = None
        self.class_and_method = None

    def _assemble_problem_string_and_filename(self) -> None:
        """
        Use the requester's data to assemble the problem title string
        """
        if not self._requester.question_num:
            raise AttributeError("Could not determine question number")
        if not self._requester.question_title:
            raise AttributeError("Could not determine question title")

        self.problem_string = f'{self._requester.question_num}. {self._requester.question_title}'
        if not self.filename:
            self.filename = f'p{self._requester.question_num}-{self._requester.slug}.py'
            self.filepath = os.path.join(os.path.abspath(self.directory), self.filename)

    def _assemble_code(self) -> None:
        """
        Use requester's code snippet to assemble code content
        """
        if not self._requester.code_snippets:
            raise AttributeError("Could not find starting code snippets")

        if self._requester.code_snippets.get("python3"):
            self.class_and_method = self._requester.code_snippets["python3"]["code"]
        else:
            raise KeyError("Could not find starting Python 3 code snippet")
        
        # Pattern to ID class name
        class_pattern = r'class (?P<classname>\w+)\([\w\s:\[\],]+?\)?:'
        class_match = re_search(class_pattern, self.class_and_method)

        if class_match:
            self.classname = class_match.group("classname")
        
        # Pattern to ID and extract the method definition
        method_def_pattern = r'def\s+(?P<method_name>\w+)\(([\w\s:\[\],]+)?\)(\s->[\s\w\[\]]+)?:'
        method_match = re_search(method_def_pattern, self.class_and_method)

        if not method_match:
            raise Exception("Method definition could not be parsed:", self.class_and_method)

        self.method_name = method_match.group("method_name")
    
        # Pattern to look for typing imports
        typing_pattern = r'(List|Optional)\[\w+\]'
        self.typing_imports = set(findall(typing_pattern, self.class_and_method))

    def request(self) -> None:
        # Request and process data from Leetcode
        self._requester.request()
        self._assemble_problem_string_and_filename()

        # Check if a file already exists with the same name
        if os.path.exists(self.filepath):
            raise FileExistsError

        self._assemble_code()

    def write_file(self) -> None:
        try:
            if not self.filepath:
                raise ValueError("File path is undefined")
            if not self.problem_string:
                raise ValueError("Problem title and number missing")
            if not self.class_and_method:
                raise ValueError("Problem class and method missing")

            with open(self.filepath, 'w') as file:
                # Write headers and imports
                file.write(f'# {self.problem_string}\n')
                file.write('import unittest\n')
                # Include imports for data structures
                if self.data_structure:
                    file.write(DATA_STRUCTURE_IMPORTS[self.data_structure])
                if self.typing_imports:
                    file.write(f'from typing import {", ".join(sorted(self.typing_imports))}\n')
                file.write('\n\n')

                # Write solution class and method
                file.write(self.class_and_method)
                file.write('pass\n\n\n')
                
                # Write solution test case
                file.write(f"class {self.classname}Test(unittest.TestCase):\n")
                file.write(f"{INDENT}def setUp(self) -> None:\n")
                file.write(f"{INDENT}{INDENT}sol = {self.classname}()\n")
                if self.method_name:
                    file.write(f'{INDENT}{INDENT}self.solution = sol.{self.method_name}\n')
                if self.data_structure:
                    file.write(f'{2*INDENT}{DATA_STRUCTURE_TEST[self.data_structure]}\n')
                file.write(f"{INDENT}{INDENT}return super().setUp()\n\n\n")

                # Write main
                file.write("if __name__ == '__main__':\n")
                file.write(f"{INDENT}unittest.main()")

        except Exception as error:
            if self.filepath:
                os.remove(self.filepath)
            print(f'\n{type(error).__name__} {error}')
            print("The file couldn't be written. Operation aborted")


if __name__ == "__main__":

    parser=argparse.ArgumentParser(
        description="Creates a new Python 3 file with complete boilerplate for a new Leetcode problem that comes with unit testing and support for Leetcode's classes of certain data structures."
    )

    parser.add_argument("--directory", help="The directory to create the new file. Default value is the current working directory", default=".")
    parser.add_argument("--data-structure", help="Data structure to include.", choices=[None, "linked_list", "tree"])
    parser.add_argument("--filename", help="Provide a manual filename. A filename will be generated in the format 'p#-problem_name.py' if not provided")

    args=parser.parse_args()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Copy and paste the complete Leetcode URL:")
    leetcode_url = input()

    try:
        problem = Problem(leetcode_url, **vars(args))
        problem.request()
        problem.write_file()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\nFile created at {os.path.relpath(problem.filepath)}\n')
    except FileExistsError as error:
        print(f'\nFILE ERROR: A file with the same file name already exists. Please use the --filename argument to provide a custom filename\n')
    except Exception as error:
        print(f'{type(error)}: {error}')