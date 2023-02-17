# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CreateAirlineReservationWizard(models.TransientModel):
    _name = "create.reservation.wizard"
    _description = "Create Reservation  Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CreateAirlineReservationWizard, self).default_get(fields)
        if self.env.context.get('active_id'):
            res['product_id'] = self.env.context.get('active_id')
            
        return res

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    passenger_ids = fields.Many2many('travel_tour_agency.passenger',                               
                                domain="[('partner_id','=',partner_id)]")  
    product_id =   fields.Many2one('product.template')
    book_type  = fields.Selection(  related="product_id.book_type" )

    def action_create_reservation(self):
        vals={}
        if self.book_type ==  'airline':

            vals = {
                'partner_id': self.partner_id.id,
                'passenger_ids':self.passenger_ids,
                'airlines_ids':[(0,0,{'product_id':self.product_id.id})],
                'airline_service':True
            }
        else:
            vals = {
                'partner_id': self.partner_id.id,
                'passenger_ids':self.passenger_ids,
                'hotels_ids':[(0,0,{'product_id':self.product_id.id})],
                'hotel_service':True
            }
        reservation_rec = self.env['travel_tour_agency.reservation'].create(vals)
        return {
            'name': _('Reservation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'travel_tour_agency.reservation',
            'res_id': reservation_rec.id,
        }

    