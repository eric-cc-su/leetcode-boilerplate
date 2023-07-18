import unittest

from src.components.LinkedList import LinkedList, ListNode

class LinkedListClassTest(unittest.TestCase):
    """
    Test the LinkedList class
    """
    def testObjListInit(self) -> None:
        """
        Tests initialization with an object list
        """
        test_list = [1,2,3,4,5]
        ll = LinkedList(object_list=test_list)
        self.assertIsInstance(ll, LinkedList)
        self.assertIsInstance(ll.head, ListNode)
        self.assertListEqual(ll.obj_list, test_list)
        self.assertEqual(ll.head.val, test_list[0])

    def testHeadInit(self) -> None:
        """
        Tests initialization with a ListNode head object
        """
        node = ListNode(1, ListNode(2, ListNode(3)))
        ll = LinkedList(head_node=node)
        self.assertIsInstance(ll, LinkedList)
        self.assertIsInstance(ll.head, ListNode)
        self.assertIsNone(ll.obj_list)
        self.assertEqual(ll.head.val, node.val)

    def testDualInit(self) -> None:
        """
        Tests attempts to initialize with both an object list and a ListNode.
        Expects an error.
        """
        test_list = [1,2,3,4,5]
        node = ListNode(1, ListNode(2, ListNode(3)))
        ll = None
        with self.assertRaises(ValueError):
            ll = LinkedList(object_list=test_list, head_node=node)
        self.assertIsNone(ll)

    def testNonListInit(self) -> None:
        """
        Tests initialization with an invalid non-list type
        """
        ll = None
        with self.assertRaises(TypeError):
            ll = LinkedList(object_list=1)
        self.assertIsNone(ll)


class LinkedListConversionTestMethods(unittest.TestCase):
    """
    Methods to test the utility function convertListToLinkedList
    """
    def setUp(self) -> None:
        self.default_list = [1,2,3,4,5]
        self.ll = LinkedList(object_list=self.default_list)
        self.ll.head = self.ll.head
        return super().setUp()
    
    def testLinked(self):
        """
        Tests that the head has actually been connected to another node
        """
        self.assertIsNotNone(self.ll.head.next)
        self.assertIsInstance(self.ll.head.next, ListNode)
        self.assertEqual(self.ll.head.next.val, self.default_list[1])
    
    def testCorrect(self):
        """
        Tests that the linked list has been created with all nodes in the expected order
        """
        self.ll.assertListEqual(self, self.default_list)
