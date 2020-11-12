# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestOddoorIot(TransactionCase):
    def setUp(self):
        super(TestOddoorIot, self).setUp()
        self.template = self.browse_ref("oddoor_iot.oddoor_template")
        self.group_1 = self.env["oddoor.group"].create({"name": "Group 1"})
        self.group_2 = self.env["oddoor.group"].create({"name": "Group 2"})
        self.key_1 = self.env["oddoor.key"].create(
            {"name": "Key 1", "group_ids": [(4, self.group_1.id)]}
        )
        self.key_2 = self.env["oddoor.key"].create(
            {"name": "Key 2", "group_ids": [(4, self.group_2.id)]}
        )

    def test_oddoor_iot(self):
        configure = self.env["iot.device.configure"].create({})
        configure.run()
        result = self.env["iot.device.configure"].configure(
            configure.serial, self.template.name
        )
        call_lock_info = result["inputs"]["call_lock"]
        call_lock = self.env["iot.device.input"].get_device(
            call_lock_info["serial"], call_lock_info["passphrase"]
        )
        self.assertTrue(call_lock)
        call_lock_values_info = result["inputs"]["call_lock_values"]
        call_lock_values = self.env["iot.device.input"].get_device(
            call_lock_values_info["serial"],
            call_lock_values_info["passphrase"],
        )
        self.assertTrue(call_lock_values)
        self.assertNotEqual(call_lock, call_lock_values)
        self.assertEqual(call_lock.device_id, call_lock_values.device_id)
        self.assertEqual(call_lock.lock_id, call_lock_values.lock_id)
        lock = call_lock.lock_id
        self.assertFalse(lock.action_ids)
        lock.group_ids = self.group_1
        result = call_lock.call_device(self.key_1.unique_virtual_key)
        self.assertTrue(result["access_granted"])
        self.assertTrue(lock.action_ids)
        self.assertEqual(1, len(lock.action_ids))
        result = call_lock.call_device(self.key_2.unique_virtual_key)
        self.assertFalse(result["access_granted"])
        self.assertEqual(2, len(lock.action_ids))
        result = call_lock_values.call_device("")
        found = False
        for key in result["keys"]:
            if key["unique_virtual_key"] == self.key_1.unique_virtual_key:
                found = True
                break
        self.assertTrue(found)
        found = False
        for key in result["keys"]:
            if key["unique_virtual_key"] == self.key_2.unique_virtual_key:
                found = True
                break
        self.assertFalse(found)
