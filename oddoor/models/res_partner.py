# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    oddoor_key_ids = fields.One2many("oddoor.key", inverse_name="partner_id")
    oddoor_key_count = fields.Integer(compute="_compute_oddoor_key_count")

    @api.depends("oddoor_key_ids")
    def _compute_oddoor_key_count(self):
        for record in self:
            record.oddoor_key_count = len(record.oddoor_key_ids)

    def action_view_oddoor_key(self):
        self.ensure_one()
        action = self.env.ref("oddoor.oddoor_key_act_window").read()[0]
        action["domain"] = [("partner_id", "=", self.id)]
        action["context"] = {"default_partner_id": self.id}
        return action
