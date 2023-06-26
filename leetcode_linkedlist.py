import unittest

from typing import List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def convertListToLinkedList(self, normlist: List[int]):
        """
        Converts the given Python list into a linked list
        """
        head = None
        for item in reversed(normlist):
            if head is None:
                head = ListNode(val=item)
            else:
                newhead = ListNode(val=item, next=head)
                head = newhead

        return head
    
    def assertLinkedListEqual(self, testcase: unittest.TestCase, linked_list: ListNode, expected: List[int]):
        """
        Checks whether the given linked list in the form of a ListNode is equal to the expectation given as a list of ints
        """
        test_head = linked_list
        length = 0
        for element in expected:
            length += 1
            testcase.assertEqual(test_head.val, element)
            test_head = test_head.next
        
        testcase.assertIsNone(test_head)
        testcase.assertEqual(length, len(expected))


class LinkedListConversionTestMethods(unittest.TestCase):
    """
    Methods to test the utility function convertListToLinkedList
    """
    def setUp(self) -> None:
        self.default_list = [1,2,3,4,5]
        self.ll = LinkedList()
        self.ll_head = self.ll.convertListToLinkedList(self.default_list)
        return super().setUp()

    def testInstance(self):
        """
        Tests that a linked list node has indeed been returned
        """
        self.assertIsInstance(self.ll_head, ListNode)
    
    def testReturnHead(self):
        """
        Tests that the expected head of the linked list has been returned. (Checks node.val)
        """
        self.assertEqual(self.ll_head.val, self.default_list[0])
    
    def testLinked(self):
        """
        Tests that the head has actually been connected to another node
        """
        self.assertIsNotNone(self.ll_head.next)
        self.assertIsInstance(self.ll_head.next, ListNode)
    
    def testCorrect(self):
        """
        Tests that the linked list has been created with all nodes in the expected order
        """
        self.ll.assertLinkedListEqual(self, self.ll_head, self.default_list)


if __name__ == "__main__":
    unittest.main()