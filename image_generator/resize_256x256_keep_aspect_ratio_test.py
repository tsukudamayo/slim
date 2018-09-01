import unittest
import numpy as np
from resize_256x256_keep_aspect_ratio import difference_to_target


class TestSweet(unittest.TestCase):

    def test_difference_to_target_x_is_bigger(self):
        target = tuple((224,224))
        print('target', target)
        test = tuple((448,672))
        print('test', test)

        result = difference_to_target(test, target)
        expected = tuple((149, 224))
        self.assertTupleEqual(result, expected)

    def test_difference_to_target_x_is_lower(self):
        target = tuple((224,224))
        print('target', target)
        test = tuple((112,56))
        print('test', test)

        result = difference_to_target(test, target)
        expected = tuple((224,112))
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
        
        

        


















        
