import unittest
import sys
import os
sys.path.append(os.path.abspath("src"))

from nlang import run

class TestVirtualMachine(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple_script(self):
        code = """
            x = 10
            y = 20
            result = x + y
            print(result)
        """
        result = run(code, debug=False)
        self.assertEqual(result, 30)
    
    def test_loop_script(self):
        code = """
            x = 0
            while x < 5:
                x = x + 1
            print(x)
        """
        result = run(code, debug=False)
        self.assertEqual(result, 5)
    
    def test_conditional_script(self):
        code = """
            if 1 < 2:
                print("yes")
            else:
                print("no")
        """
        result = run(code, debug=False)
        self.assertEqual(result, "yes")
      
if __name__ == '__main__':
    unittest.main()
