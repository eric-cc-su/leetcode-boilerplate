# A script to create the boilerplate for a new Leetcode problem that comes with unit testing 
#
# Python 3.6+ required
#
# Inputs:
# 1. The problem number
# 2. The file name
# 3. The full problem name (For display purposes)
# 4. Whether the solution needs to be encased in a class (default to True)
# 5. The solution method name
# 6. copy-paste of method declaration
import argparse
import os

from re import match as re_match, sub as re_sub
from sys import argv
from typing import Optional

# Constant for how to indent (currently using one tab equals four spaces)
INDENT = "    "

DATA_STRUCTURE_IMPORTS = {
    'linked_list': 'from leetcode_linkedlist import LinkedList, ListNode\nfrom typing import Optional\n\n',
    'tree': 'from leetcode_treenode import Tree, TreeNode\nfrom typing import Optional\n\n',
}

DATA_STRUCTURE_TEST = {
    'linked_list': 'self.ll = LinkedList()',
    'tree': 'self.tree = Tree()'
}


class Problem:
    def __init__(self, problem_string: str, method_def: str,
                 directory: Optional[str]=".",
                 classname: Optional[str]=None, no_encase: Optional[bool]=False,
                 data_structure: Optional[str]=None, filename: Optional[str]=None) -> None:
        self.problem_string = problem_string
        self.parse_problem_string()
        
        self.method_def = method_def
        self.parse_method_definition()

        self.classname = "Solution" if classname is None else classname

        if data_structure and data_structure not in DATA_STRUCTURE_IMPORTS.keys():
            raise ValueError(f"Data structure {data_structure} not supported")
        self.data_structure = data_structure

        self.encase = not no_encase
        
        if filename:
            self.filename = filename
        self.filepath = os.path.join(os.path.abspath(directory), self.filename)

        # Check if a file already exists with the same name
        if os.path.exists(self.filepath):
            raise FileExistsError

    def parse_problem_string(self) -> None:
        """
        Parse the problem string to create the filename and correct spacing issues
        """
        pattern = r'(?P<problem_num>\d+)(?P<period>\.)?(?P<leading_space>\s)?(?P<problem_name>[\w\s]+)'
        match = re_match(pattern, self.problem_string)

        if not match:
            raise Exception("Problem string could not be parsed")

        # Correct problem string
        problem_words = re_sub(r'\s+', ' ', match.group("problem_name"))
        self.problem_string = f'{match.group("problem_num")}. {problem_words}'
        
        # Create filename in format 'p123-problem_name.py'
        filename_words = re_sub(r'\s+','_',match.group("problem_name").lower())
        self.filename = f'p{match.group("problem_num")}-{filename_words}.py'
    
    def parse_method_definition(self) -> None:
        """
        Parse the method definition string.

        Now supports blank method definition and makes no assumption about what method the user wants.

        This is applicable for problems where the solution is a custom class.
        """
        pattern = r'def\s+(?P<method_name>\w+)\(([\w\s:\[\],]+)?\)(\s->[\s\w\[\]]+)?:'
        
        self.method_def = self.method_def.strip(' ')
        
        if not self.method_def:
            self.method_name = None
            return
        
        method_match = re_match(pattern, self.method_def)

        if not method_match:
            raise Exception("Method definition could not be parsed")

        self.method_name = method_match.group("method_name")

    def write_file(self) -> None:
        try:
            with open(self.filepath, 'w') as file:
                # Write headers and imports
                file.write(f'# {self.problem_string}\n')
                # Include imports for data structures
                if self.data_structure:
                    file.write(DATA_STRUCTURE_IMPORTS[self.data_structure])
                file.write('import unittest\n\n\n')

                # Write solution class
                if self.encase:
                    file.write(f'class {self.classname}:\n')
                
                # Write solution method if provided
                if self.method_def:
                    method_dec_str = f'{self.method_def}\n'
                    if self.encase:
                        method_dec_str = INDENT + method_dec_str
                    file.write(method_dec_str)
                    file.write(f"{2*INDENT}pass\n\n\n")
                else:
                    file.write(f"{INDENT}pass\n\n" + ("\n" if self.encase else ""))
            
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
            os.remove(self.filename)
            print(f'\n{type(error).__name__} {error}')
            print("The file couldn't be written. Operation aborted")


if __name__ == "__main__":

    parser=argparse.ArgumentParser(
        description="Creates a new Python 3 file with complete boilerplate for a new Leetcode problem that comes with unit testing and support for Leetcode's classes of certain data structures."
    )

    parser.add_argument("--directory", help="The directory to create the new file. Default value is the current working directory", default=".")
    parser.add_argument("--classname", help='Provide a manual name for the solution class. Default value is "Solution"', default="Solution")
    parser.add_argument("--data-structure", help="Data structure to include.", choices=[None, "linked_list", "tree"])
    parser.add_argument("--filename", help="Provide a manual filename. A filename will be generated in the format 'p#-problem_name.py' if not provided")
    parser.add_argument("--no-encase", help="Do not encase the solution in a class", action="store_true")

    args=parser.parse_args()

    print("Copy and paste the problem headliner (ex. '123. Hello World')")
    problem_string = input()
    
    print("Copy and paste the method definition (ex. 'def helloWorld(self, args...):')")
    method_def = input()

    try:
        problem = Problem(problem_string, method_def, **vars(args))
        problem.write_file()
        print(f'File created at {problem.filename}\n')
    except FileExistsError as error:
        print(f'ERROR: A file with the same file name already exists. Please use the --filename argument to provide a custom filename\n')
    except Exception as error:
        print(f'ERROR: {error}')