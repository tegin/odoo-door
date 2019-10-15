# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OddoorGroup(models.Model):

    _name = 'oddoor.group'
    _description = 'Oddoor Group'

    name = fields.Char()
    active = fields.Boolean(default=True, required=True)
    lock_ids = fields.Many2many('oddoor.lock', string="Locks")
    parent_ids = fields.Many2many(
        'oddoor.group',
        relation='oddoor_group_implied_rel',
        column1='group_id',
        column2='implied_group_id',
    )

    def _check_access(self, key):
        if key.expiration_date and key.expiration_date < fields.Datetime.now():
            return False
        return self._check_access_recursion(key)

    def _check_access_recursion(self, key, limit=0):
        if not self:
            return False
        if limit > 50:
            return False
        if self & key.group_ids:
            return True
        return self.mapped('parent_ids')._check_access_recursion(key, limit+1)

    @api.constrains('parent_ids')
    def _check_recursion_parent_ids(self):
        if not self._check_m2m_recursion('parent_ids'):
            raise ValidationError(_('A recurssion was found'))
