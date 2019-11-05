# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MedicalEncounter(models.Model):

    _inherit = 'medical.encounter'

    door_key = fields.Char()

    @api.multi
    def generate_surgical_key(self):
        self.ensure_one()
        self.door_key = self.env['oddoor.key'].create({
            'name': 'Surgical key for %s' % self.patient_id.name,
            'group_ids': self.env.ref('oddor_encounter.group_surgical')
        })
