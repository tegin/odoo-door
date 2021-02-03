# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = ["hr.employee", "oddoor.key.mixin"]

    oddoor_key_id = fields.Many2one(
        "oddoor.key", compute="_compute_oddoor_key"
    )
    oddoor_key_ids = fields.One2many(
        context={"active_test": False}, string="Oddoor Keys"
    )
    group_ids = fields.Many2many(
        "oddoor.group",
        related="oddoor_key_id.group_ids",
        readonly=False,
        string="Oddoor groups",
    )
    rfid_card_code = fields.Char(
        store=True,
        compute="_compute_rfid_card_code",
        inverse="_inverse_rfid_card_code",
    )

    @api.depends("oddoor_key_ids.unique_virtual_key", "oddoor_key_ids")
    def _compute_rfid_card_code(self):
        for record in self:
            if record.oddoor_key_ids:
                record.rfid_card_code = (
                    record.oddoor_key_ids.unique_virtual_key
                )

    def _inverse_rfid_card_code(self):
        for record in self:
            if record.oddoor_key_ids:
                record.oddoor_key_ids.unique_virtual_key = (
                    record.rfid_card_code
                )

    @api.depends("oddoor_key_ids")
    def _compute_oddoor_key(self):
        for record in self:
            record.oddoor_key_id = record.oddoor_key_ids

    def _generate_oddoor_key_vals(self):
        return {
            "unique_virtual_key": self.rfid_card_code,
            "name": _("Key of %s") % self.display_name,
            "res_id": self.id,
            "res_model": self._name,
        }

    def generate_oddoor_key(self):
        self.ensure_one()
        if not self.oddoor_key_id and self.rfid_card_code:
            self.env["oddoor.key"].create(self._generate_oddoor_key_vals())
            self.refresh()
            self._compute_rfid_card_code()
        return {}
