from datetime import date
from odoo import models, fields, api






class Customer(models.Model):
    _inherit = 'res.partner'


    passenger_ids = fields.One2many('travel_tour_agency.passenger', 'partner_id',
                                            string="Passengers")
    whatsApp   = fields.Char(string="WhatsApp")
    # reservation_ids= fields.One2many('travel_tour.reservation', 'partner_id',
    #                                         string="Reservations")

    def btn_whatsapp(self,message= 'Hello'):
         
        if self.whatsApp:
            wa_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.whatsApp,message)
        else:
            wa_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.phone,message)

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url':wa_api_url
        }
