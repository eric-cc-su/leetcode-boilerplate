import unittest

from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Tree:
    def assembleTreeFromList(self, array: List[int]) -> Optional[TreeNode]:
        if not array:
            return None
        
        node = TreeNode(array.pop(0))
        root = node
        queue = []

        skip_left = False
        while array:
            val = array.pop(0)
            if not skip_left and node.left is None:
                if val is None:
                    skip_left = True
                    continue
                else:
                    node.left = TreeNode(val)
                    queue.append(node.left)
            # elif node.right is None:
            else:
                if skip_left == True:
                    skip_left = False
                if val:
                    node.right = TreeNode(val)
                    queue.append(node.right)
                # move on to the next node expecting children
                node = queue.pop(0)
        
        return root

    def assertTreeEqual(self, testcase: unittest.TestCase, root: TreeNode, expected: List[int]):
        """
        Checks whether the given Tree in the form of a TreeNode is equal to the expectation given as a list of ints
        """
        # test_head = root
        traversal_queue = [root]
        # expected acts as a queue
        while expected:
            # TODO: Handle trees that can allow missing leaves
            node = traversal_queue.pop(0)
            expected_val = expected.pop(0)
            testcase.assertIsNotNone(node)
            testcase.assertEqual(node.val, expected_val)
        
            if node.left:
                traversal_queue.append(node.left)
            if node.right:
                traversal_queue.append(node.right)
        
        traversal_queue = list(filter(lambda item: item is not None, traversal_queue))
        testcase.assertEqual(len(traversal_queue), 0)


class TreeAssemblyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = Tree()
        self.simple_tree_array = [1,2,3]
        return super().setUp()

    def testInstance(self) -> None:
        self.assertIsInstance(self.tree.assembleTreeFromList(self.simple_tree_array), TreeNode)
    
    def testNodes(self) -> None:
        root = self.tree.assembleTreeFromList(self.simple_tree_array)
        self.assertEqual(root.val, 1)
        self.assertIsNotNone(root.left)
        self.assertIsInstance(root.left, TreeNode)
        self.assertIsNotNone(root.right)
        self.assertIsInstance(root.right, TreeNode)

        self.assertEqual(root.left.val, 2)
        self.assertEqual(root.right.val, 3)

    def testEmptyList(self) -> None:
        # We want to support an empty list under the edge case where we need an empty TreeNode
        root = self.tree.assembleTreeFromList([])
        self.assertIsNone(root)

    def testRightNone(self) -> None:
        root = self.tree.assembleTreeFromList([1,2,None])
        self.assertEqual(root.val, 1)
        self.assertIsInstance(root.left, TreeNode)
        self.assertEqual(root.left.val, 2)
        self.assertIsNone(root.right)

    def testLeftNoneRightExists(self) -> None:
        root = self.tree.assembleTreeFromList([1,None,2])
        self.assertEqual(root.val, 1)
        self.assertIsNone(root.left)
        self.assertIsInstance(root.right, TreeNode)
        self.assertEqual(root.right.val, 2)

    def testRightNone2(self) -> None:
        # Test a missing right leaf on a higher branch
        # We are testing to make sure the lower branches or leaves are not accidentally populated as the intentionally missing right branch
        root = self.tree.assembleTreeFromList([1,2,None,3,4])
        #
        #    1
        #   /  \
        #   2  None
        #  / \
        # 3   4
        #
        self.assertEqual(root.val, 1)
        self.assertIsInstance(root.left, TreeNode)
        self.assertEqual(root.left.val, 2)
        self.assertIsNone(root.right)

        self.assertIsInstance(root.left.left, TreeNode)
        self.assertEqual(root.left.left.val, 3)
        self.assertIsInstance(root.left.right, TreeNode)
        self.assertEqual(root.left.right.val, 4)
    
    def testLeftNone2(self) -> None:
        # Test a missing left leaf on a higher branch
        # We are testing to make sure the lower branches or leaves are not accidentally populated as the intentionally missing left branch
        root = self.tree.assembleTreeFromList([1,None,2,3,4])
        #
        #    1
        #   /  \
        # None  2
        #      / \
        #     3   4
        #
        self.assertEqual(root.val, 1)
        self.assertIsNone(root.left)
        self.assertIsInstance(root.right, TreeNode)
        self.assertEqual(root.right.val, 2)

        self.assertIsInstance(root.right.left, TreeNode)
        self.assertEqual(root.right.left.val, 3)
        self.assertIsInstance(root.right.right, TreeNode)
        self.assertEqual(root.right.right.val, 4)


if __name__ == "__main__":
    unittest.main()