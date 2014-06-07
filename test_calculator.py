from django.test import TestCase
from calculator import utilities

class TestCalculator(TestCase):
    def test_plus(self):
        result = utilities.process_string("fifty three plus twenty one")
        self.assertEqual(74, result)
        
    def test_minus(self):
        result = utilities.process_string("fifty three minus twenty one")
        self.assertEqual(32, result)
        
    def test_multiply(self):
        result = utilities.process_string("fifty three times twenty one")
        self.assertEqual(1113, result)
        
    def test_divide(self):
        result = utilities.process_string("fifty four \ twenty seven")
        self.assertEqual(2, result)
        
    def test_mod(self):
        result = utilities.process_string("fifty three mod twenty one")
        self.assertEqual(11, result)
        
    def test_decimals(self):
        nstring = 'two point one three plus four dot zero seven one'
        result = utilities.process_string(nstring)
        self.assertEqual(6.201, result)
        
    def test_spacing(self):
        nstring = 'twohundredthousandninehundredandfourminussixtysix'
        result = utilities.process_string(nstring)
        self.assertEqual(200838, result)    
        
    def test_mixed(self):
        nstring = '30 thousand 800 seventy four'
        result = utilities.process_string(nstring)
        self.assertEqual(30874, result)
        
    def test_unordered(self):
        nstring = 'four million three hundred thousand one hundred and seventy four'
        result = utilities.process_string(nstring)
        self.assertEqual(4300174, result)
        
    def test_places(self):
        nstring = 'two trillion four billion eighty eight million nine thousand five hundred ninety two'
        result = utilities.process_string(nstring)
        self.assertEqual(2004088009592, result)
        
    def test_order_of_operations(self):
        nstring = 'three ** (four minus two) * one plus two'
        result = utilities.process_string(nstring)
        self.assertEqual(11, result)

    def test_consecutive_digits(self):
        nstring = '12 4'
        result = utilities.process_string(nstring)
        self.assertIsNone(result)
    
    def test_incorrect_ascending(self):
        nstring = 'four eighty one'
        result = utilities.process_string(nstring)
        self.assertIsNone(result)

    def test_incorrect_descending(self):
        nstring = 'four one'
        result = utilities.process_string(nstring)
        self.assertIsNone(result)

    def test_incorrect_descending2(self):
        nstring = 'ten one'
        result = utilities.process_string(nstring)
        self.assertIsNone(result)


    def test_incorrect_descending3(self):
        nstring = '430 twenty eight'
        result = utilities.process_string(nstring)
        self.assertIsNone(result)



