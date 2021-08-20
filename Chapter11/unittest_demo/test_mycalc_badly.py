import mycalc
import unittest


class TestMyCalc(unittest.TestCase):

  def test_add(self):
    mc = mycalc.MyCalc(1, 10)
    assert mc.add() == 11

    # much better error output
    self.assertEqual(mc.add(), 12)

if __name__ == '__main__':
  unittest.main()
