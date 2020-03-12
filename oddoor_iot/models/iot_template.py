# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IotTemplate(models.Model):
    _inherit = 'iot.template'

    @api.multi
    def _get_keys(self, serial):
        result = super()._get_keys(serial)
        if self == self.env.ref('oddoor_iot.oddoor_template'):
            lock = self.env['oddoor.lock'].create({
                'name': serial
            })
            result.update({
                'lock_id': lock.id,
            })
        import logging
        logging.info(result)
        return result
