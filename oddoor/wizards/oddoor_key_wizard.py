# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class OddoorKeyWizard(models.TransientModel):

    _name = "oddoor.key.wizard"
    _description = "Create a Key"

    res_id = fields.Integer(required=True)
    res_model = fields.Char(required=True)
    oddoor_key_id = fields.Many2one("oddoor.key",)
    unique_virtual_key = fields.Char(required=True)
    group_ids = fields.Many2many("oddoor.group")

    def _create_oddoor_vals(self):
        record = self.env[self.res_model].browse(self.res_id)
        return {
            "res_id": self.res_id,
            "res_model": self.res_model,
            "name": _("Key of %s") % record.display_name,
            "unique_virtual_key": self.unique_virtual_key,
            "group_ids": [(6, 0, self.group_ids.ids)],
        }

    def create_key(self):
        self.ensure_one()
        if not self.oddoor_key_id:
            self.oddoor_key_id = self.env["oddoor.key"].create(
                self._create_oddoor_vals()
            )
        return self.update_key(False)

    def _update_key_vals(self):
        record = self.env[self.res_model].browse(self.res_id)
        return {
            "unique_virtual_key": self.unique_virtual_key,
            "name": _("Key of %s") % record.display_name,
            "group_ids": [(6, 0, self.group_ids.ids)],
        }

    def update_key(self, update=True):
        if update:
            self.oddoor_key_id.write(self._update_key_vals())
        return {}
