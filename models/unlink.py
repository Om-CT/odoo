from odoo import models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def unlink(self):
        for order in self:
          
            if order.state in ('sale', 'done'):
                raise UserError(_("You cannot delete a confirmed  order: %s") % order.name)
            
          
            print(f"Deleting order: {order.name}")

 
        return super().unlink()
