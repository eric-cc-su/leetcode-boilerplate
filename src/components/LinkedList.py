import unittest

from typing import List, Optional

class ListNode:
    """
    Leetcode's representation of a linked list node
    """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    """
    A representation of a Leetcode linked list.

    Primarily created for testing purposes.
    Includes static methods if a full LinkedList instance is not desired. Leetcode does not use a full LinkedList class
    so this entire class is unopinionated.
    """
    def __init__(self, object_list: Optional[List[any]]=None, head_node: Optional[ListNode]=None) -> None:
        if object_list and head_node:
            raise ValueError("Both an object list and a head were provided. Please initialize with one or the other, not both")
        self.head = head_node
        self.obj_list = object_list

        if self.obj_list:
            self.setWithList(self.obj_list)
        elif self.obj_list is not None:
            raise TypeError(f"Cannot initialize with non-list type {type(self.obj_list)}")

    @staticmethod
    def convertListToLinkedList(normlist: List[int]) -> ListNode:
        """
        Converts the given Python list into a linked list and returns the head node
        """
        if type(normlist) != list:
            raise TypeError(f"Cannot convert non-list type: {type(normlist)}")
        head = None
        for item in reversed(normlist):
            if head is None:
                head = ListNode(val=item)
            else:
                newhead = ListNode(val=item, next=head)
                head = newhead

        return head
    
    def setWithList(self, normlist: List[int]) -> None:
        """
        Public method to set the entire linked list with a normal object list
        """
        self.obj_list = normlist
        self.head = LinkedList.convertListToLinkedList(normlist)

    @staticmethod
    def assertLinkedListEqual(testcase: unittest.TestCase, head: ListNode, expected: List[int]):
        """
        Checks whether the given linked list in the form of a ListNode is equal to the expectation given as a list of ints
        """
        test_head = head
        length = 0
        for element in expected:
            length += 1
            testcase.assertEqual(test_head.val, element)
            test_head = test_head.next
        
        testcase.assertIsNone(test_head)
        testcase.assertEqual(length, len(expected))

    def assertListEqual(self, testcase: unittest.TestCase, expected: List[int]):
        """
        Checks whether the current instance's linked list is equal to the expected list of objects
        """
        head = self.head
        LinkedList.assertLinkedListEqual(testcase, self.head, expected)
        self.head = head