# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo.fields import Datetime
from odoo.tests.common import SavepointCase


class TestOddoor(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestOddoor, cls).setUpClass()

        cls.group_1 = cls.env["oddoor.group"].create({"name": "Group 1"})
        cls.group_2 = cls.env["oddoor.group"].create({"name": "Group 2"})
        cls.lock = cls.env["oddoor.lock"].create(
            {"name": "Lock", "group_ids": [(4, cls.group_1.id)]}
        )
        cls.key_1 = cls.env["oddoor.key"].create(
            {"name": "Key 1", "group_ids": [(4, cls.group_1.id)]}
        )
        cls.key_2 = cls.env["oddoor.key"].create(
            {"name": "Key 2", "group_ids": [(4, cls.group_2.id)]}
        )

    def test_allowed_access(self):
        self.assertTrue(
            self.lock.check_access_unique_virtual_key(
                self.key_1.unique_virtual_key
            )
        )

    def test_not_allowed_access(self):
        self.assertFalse(
            self.lock.check_access_unique_virtual_key(
                self.key_2.unique_virtual_key
            )
        )

    def test_non_existing_key(self):
        self.assertFalse(self.lock.action_ids)
        self.assertFalse(
            self.lock.check_access_unique_virtual_key(
                self.key_1.unique_virtual_key + self.key_2.unique_virtual_key
            )
        )
        self.assertTrue(self.lock.action_ids)
        self.assertFalse(self.lock.action_ids.key_id)

    def test_inheritance(self):
        self.group_1.parent_ids = [(4, self.group_2.id)]
        self.assertTrue(
            self.lock.check_access_unique_virtual_key(
                self.key_2.unique_virtual_key
            )
        )

    def test_inheritance_loop(self):
        group = self.env["oddoor.group"].create({"name": "Group 1 0"})
        self.group_1.parent_ids = [(4, group.id)]
        for i in range(0, 50):
            key = self.env["oddoor.key"].create(
                {"name": "Key 2", "group_ids": [(4, group.id)]}
            )
            self.assertTrue(
                self.lock.check_access_unique_virtual_key(
                    key.unique_virtual_key
                )
            )
            new_group = self.env["oddoor.group"].create(
                {"name": "Group 1 %s" % i}
            )
            group.parent_ids = [(4, new_group.id)]
            group = new_group
        key = self.env["oddoor.key"].create(
            {"name": "Key 2", "group_ids": [(4, group.id)]}
        )
        self.assertFalse(
            self.lock.check_access_unique_virtual_key(key.unique_virtual_key)
        )

    def test_recursion(self):
        self.group_1.parent_ids = [(4, self.group_2.id)]
        with self.assertRaises(ValidationError):
            self.group_2.parent_ids = [(4, self.group_1.id)]

    def test_actions(self):
        self.assertFalse(self.key_1.action_ids)
        self.assertFalse(self.lock.action_ids)
        self.lock.check_access_unique_virtual_key(
            self.key_1.unique_virtual_key
        )
        self.assertTrue(self.key_1.action_ids)
        self.assertTrue(self.lock.action_ids)
        self.assertFalse(self.key_2.action_ids)
        self.lock.check_access_unique_virtual_key(
            self.key_2.unique_virtual_key
        )
        self.assertTrue(self.key_2.action_ids)
        action = self.lock.view_actions()
        self.assertEqual(
            self.lock.action_ids,
            self.env[action["res_model"]].search(action["domain"]),
        )
        action = self.key_1.view_actions()
        self.assertEqual(
            self.env[action["res_model"]].search(action["domain"]),
            self.key_1.action_ids,
        )

    def test_expiration(self):
        self.assertTrue(
            self.lock.check_access_unique_virtual_key(
                self.key_1.unique_virtual_key
            )
        )
        now = Datetime.from_string(Datetime.now())
        self.key_1.expiration_date = Datetime.to_string(
            now + timedelta(hours=1)
        )
        self.assertTrue(
            self.lock.check_access_unique_virtual_key(
                self.key_1.unique_virtual_key
            )
        )
        self.key_1.expiration_date = Datetime.to_string(
            now + timedelta(hours=-1)
        )
        self.assertFalse(
            self.lock.check_access_unique_virtual_key(
                self.key_1.unique_virtual_key
            )
        )

    def test_lock_find_keys(self):
        result = self.lock.get_virtual_keys()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], self.key_1.id)
        key = self.env["oddoor.key"].create(
            {"name": "Key 1", "group_ids": [(4, self.group_1.id)]}
        )
        result = self.lock.get_virtual_keys()
        self.assertEqual(len(result), 2)
        ids = [r["id"] for r in result]
        self.assertIn(self.key_1.id, ids)
        self.assertIn(key.id, ids)
        now = Datetime.from_string(Datetime.now())
        key.expiration_date = Datetime.to_string(now + timedelta(hours=-1))
        result = self.lock.get_virtual_keys()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], self.key_1.id)
        key.expiration_date = Datetime.to_string(now + timedelta(hours=1))
        result = self.lock.get_virtual_keys()
        self.assertEqual(len(result), 2)
        ids = [r["id"] for r in result]
        self.assertIn(self.key_1.id, ids)
        self.assertIn(key.id, ids)
