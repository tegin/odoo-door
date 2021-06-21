# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OddoorLock(models.Model):

    _name = "oddoor.lock"
    _description = "Oddoor Lock"

    name = fields.Char(required=True)
    description = fields.Text()
    group_ids = fields.Many2many("oddoor.group", string="Groups")
    action_ids = fields.One2many("oddoor.key.action", inverse_name="lock_id")
    active = fields.Boolean(default=True, required=True)

    def check_access_unique_virtual_key(self, unique_virtual_key):
        self.ensure_one()
        key = self.env["oddoor.key"].search(
            [("unique_virtual_key", "=", unique_virtual_key)], limit=1
        )
        if not key:
            self._missing_key(unique_virtual_key)
            return False
        return self.check_access(key)

    def _missing_key(self, unique_virtual_key):
        return self.env["oddoor.key.action"].create(
            self._missing_key_action_vals(unique_virtual_key)
        )

    def _missing_key_action_vals(self, unique_virtual_key):
        return {
            "lock_id": self.id,
            "unique_virtual_key": unique_virtual_key,
            "result": "refused",
        }

    def check_access(self, key):
        result = self.group_ids._check_access(key)
        self.create_action(key, result)
        return result

    def create_action(self, key, result):
        return self.env["oddoor.key.action"].create(
            self._create_action_vals(key, result)
        )

    def _create_action_vals(self, key, result):
        return {
            "lock_id": self.id,
            "key_id": key.id,
            "result": "accepted" if result else "refused",
        }

    def view_actions(self):
        self.ensure_one()
        action = self.env.ref("oddoor.oddoor_key_action_act_window").read()[0]
        action["domain"] = [("lock_id", "=", self.id)]
        return action

    def get_virtual_keys(self):
        self.ensure_one()
        key_obj = self.env["oddoor.key"]
        keys = self.env["oddoor.key"]
        for group in self.group_ids:
            keys |= key_obj.search(
                [
                    ("group_ids", "=", group.id),
                    "|",
                    ("expiration_date", "=", False),
                    ("expiration_date", ">=", fields.Datetime.now()),
                ]
            )
        return keys.get_oddoor_values()
