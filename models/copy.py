from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def copy(self, default=None):
        default = dict(default or {})

        
        default['name'] = self.name + " (Copy)"

        
        return super().copy(default)
