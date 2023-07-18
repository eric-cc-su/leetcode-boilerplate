import unittest

from src.components.LinkedList import LinkedList, ListNode

class LinkedListClassTest(unittest.TestCase):
    """
    Test the LinkedList class
    """
    def testNoInit(self) -> None:
        """
        Tests initialization without any input at all
        """
        ll = LinkedList()
        self.assertIsInstance(ll, LinkedList)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.obj_list)

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

    def testSetWithList(self) -> None:
        """
        Tests the setWithList method to change the entire linked list
        """
        testlist = [1,2,3,4,5]
        ll = LinkedList()
        ll.setWithList(testlist)
        self.assertIsInstance(ll.head, ListNode)
        self.assertIsInstance(ll.obj_list, list)
        self.assertEqual(ll.head.val, testlist[0])
        self.assertListEqual(ll.obj_list, testlist)
        ll.assertListEqual(self, testlist)

        testlist2 = [9,3,2]
        ll.setWithList(testlist2)
        self.assertIsInstance(ll.head, ListNode)
        self.assertIsInstance(ll.obj_list, list)
        self.assertEqual(ll.head.val, testlist2[0])
        self.assertListEqual(ll.obj_list, testlist2)
        ll.assertListEqual(self, testlist2)


class LinkedListConversionMethods(unittest.TestCase):
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

    def testStaticConvertListToLL(self) -> None:
        """
        Tests LinkedList.convertListToLinkedList static method
        """
        head = LinkedList.convertListToLinkedList(self.default_list)
        self.assertIsInstance(head, ListNode)
        for item in self.default_list:
            self.assertEqual(item, head.val)
            head = head.next

        self.assertIsNone(head)

    def testStaticAssertLLEqual(self) -> None:
        head = LinkedList.convertListToLinkedList(self.default_list)
        self.assertIsInstance(head, ListNode)
        LinkedList.assertLinkedListEqual(self, head, self.default_list)