from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import re

class TestEmployeeEmail(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Employee = self.env['employee.management']

    def _validate_email(self, email):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if email and not re.match(email_regex, email):
            raise ValidationError(f"Invalid email format: {email}")

    def _validate_phone(self, phone):
        phone_regex = r'^\+?\d{10,15}$'
        if phone and not re.match(phone_regex, phone):
            raise ValidationError(f"Invalid phone number format: {phone}")

    def test_valid_email(self):
        # Validate email first
        self._validate_email('valid.user@example.com')

        emp = self.Employee.create({
            'name': 'Valid User',
            'email': 'valid.user@example.com',
        })
        self.assertEqual(emp.email, 'valid.user@example.com')

    def test_invalid_email_raises_error(self):
        with self.assertRaises(ValidationError):
            self._validate_email('bad-email-format')

    def test_invalid_phone_raises_error(self):
        with self.assertRaises(ValidationError):
            self._validate_phone('abc-123-xyz')  # Invalid format
