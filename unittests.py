import datetime
from unittest import TestCase
import utils


class UnitTests(TestCase):
    def test_is_str_number(self):
        self.assertTrue(utils.is_str_number("1.5"))
        self.assertTrue(utils.is_str_number("1"))
        self.assertFalse(utils.is_str_number(1)) # false - only strings can be true
        self.assertFalse(utils.is_str_number(1.5))
        self.assertFalse(utils.is_str_number("ed"))

    def test_date_coercion(self):
        self.assertEqual(utils.date_coercion("2013-12-2"), datetime.datetime(2013, 12, 2))
        self.assertEqual(utils.date_coercion("1999"), "1999")
        self.assertEqual(utils.date_coercion("10.5"), "10.5")
        self.assertEqual(utils.date_coercion("joe"), "joe")
        self.assertEqual(utils.date_coercion(2000), 2000)
        self.assertEqual(utils.date_coercion("Thursday, January 14, 2021 at 8 pm"), datetime.datetime(2021, 1, 14, 20))

