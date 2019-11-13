# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestEmployeeRfid(TransactionCase):

    def setUp(self):
        super(TestEmployeeRfid, self).setUp()
        self.employee = self.env['hr.employee'].create({
            'name': 'Employee'
        })

    def test_generate(self):
        self.employee.write({
            'rfid_card_code': '1235'
        })
        self.assertFalse(self.employee.oddoor_key_id)
        self.employee.generate_oddoor_key()
        self.assertTrue(self.employee.oddoor_key_id)
        self.assertEqual(
            self.employee.oddoor_key_id.unique_virtual_key,
            self.employee.rfid_card_code)

        self.employee.write({
            'rfid_card_code': '125466'
        })
        self.assertEqual(
            self.employee.oddoor_key_id.unique_virtual_key,
            self.employee.rfid_card_code)
