# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class OddoorKey(models.Model):
    _inherit = "oddoor.key"

    @api.model
    def _get_unique_key_models(self):
        res = super(OddoorKey, self)._get_unique_key_models()
        res.append("hr.employee")
        return res
