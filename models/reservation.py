# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class Reservation(models.Model):
    _name = 'travel_tour_agency.reservation'
    _description = 'travel_tour_agency.reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name= 'ref'



    ref = fields.Char(string="Reservation")
    pnr= fields.Char(string="PNR")
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    account_move_id = fields.Many2one('account.move', string="Invoice " ,readonly=True)
    passenger_ids = fields.Many2many('travel_tour_agency.passenger',                               
                                domain="[('partner_id','=',partner_id)]")                                                                                                  
    booking_date = fields.Date(string='Booking Date' , default=fields.Date.context_today)
    # product_id = fields.Many2many('product.template', string='Flight Seats' 
    #                        ,domain="[('book_type','=','airline'),('is_booking_type','=',True)]")
    airlines_ids = fields.One2many('reservstion.airlines','reservstion_id',string="Airline")
    hotels_ids = fields.One2many('reservstion.hotels','reservstion_id',string="Hotel")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('invoiced', 'Invoiced'),
        ('cancel', 'Cancel')], default='draft', string="Status")
    
    airline_service = fields.Boolean(string="Airline Service" , default=False)
    hotel_service = fields.Boolean(string="Hotel Service" , default=False)

    @api.model
    def create(self, vals):
        vals['ref']=self.env['ir.sequence'].next_by_code('travel_tour_agency_airline.reservation')
        res= super(Reservation, self).create(vals)
        return res
    
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    
    def confirm(self):
        for rec in self:
            rec.state = 'confirm'
                
    def create_invoice(self):
        for rec in self:
            
            invoice_line_ids=[]
            if rec.airline_service:
                for item in rec.airlines_ids:
                    product =  self.env['product.product'].search([('default_code','ilike',item.product_id.default_code)])
                    # print("***********product**********",product)
                    vals= {
                    'product_id' :product.id,
                    'name': str(item.product_id.origin.iata_code)+'-->'+str(item.product_id.destination.iata_code)    ,
                    'quantity':  item.quantity,      
                    'price_unit':item.product_id.standard_price,
                    'start_date':item.booking_start_date,
                    'end_date': item.booking_end_date,
                           }
                    # print('airline_service',vals)       
                    invoice_line_ids.append((0,0,vals)) 

            if rec.hotel_service :
                for item in rec.hotels_ids:
                    product =  self.env['product.product'].search([('default_code','ilike',item.product_id.default_code)])
                    vals= {
                    'product_id' :product.id,
                    'name': str(item.product_id.country_id.name)+'-'+str(item.product_id.city_id.name)     ,
                    'quantity':  item.quantity,      
                    'price_unit':item.product_id.standard_price,
                    'start_date':item.booking_start_date,
                    'end_date': item.booking_end_date,
                        }
                    # print('hotel_service',vals)       
                    invoice_line_ids.append((0,0,vals)) 
            if not rec.hotels_ids and not rec.airlines_ids:
                notification = {
                   'type': 'ir.actions.client',
                   'tag': 'display_notification',
                   'params': {
                       'title': _('Make Invoice'),
                       'message': "You  can't make Invoice without any services!! Add some service  ",
                       'sticky': (False),
                       }
                     }
                return notification
            if not rec.passenger_ids :
                notification = {
                   'type': 'ir.actions.client',
                   'tag': 'display_notification',
                   'params': {
                       'title': _('Make Invoice'),
                       'message': "You can't make Invoice ,at least one passenger  ",
                       'sticky': (False),
                       }
                     }
                return notification     
            out_invoice_vals = {
            'name':rec.ref,
            'move_type': 'out_invoice',
            'partner_id': rec.partner_id.id,
            'state': 'draft',
            'invoice_date': rec.booking_date,
            'invoice_payment_term_id': 1,
            'invoice_line_ids':invoice_line_ids,
            'passenger_ids':rec.passenger_ids,
            'reservation_id':rec.id,
            'pnr':rec.pnr,
            }
            out_invoice = self.env['account.move'].create(out_invoice_vals)
            rec.account_move_id=out_invoice
            rec.state = 'invoiced'
    
        return {
            'name': "reservation_invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': out_invoice.id,
        }



class ReservationAirLines(models.Model):
    _name ="reservstion.airlines"
    _description ="reservstion.airlines"

    product_id =fields.Many2one('product.template',domain="[('book_type','=','airline'),('is_booking_type','=',True)]")
    booking_start_date =  fields.Datetime(string='Departure  Date',related='product_id.booking_start_date' )
    booking_end_date =fields.Datetime(string='Arrival  Date',related='product_id.booking_end_date' )
    origin        = fields.Many2one( string="Origin",related='product_id.origin' )
    destination   = fields.Many2one(string="Destination" ,related='product_id.destination')

    list_price = fields.Float(string="Price",related='product_id.list_price')
    quantity = fields.Integer(string="Quantity" ,default=1)
    reservstion_id = fields.Many2one('travel_tour_agency.reservation', string="Reservation")


class ReservationHotels(models.Model):
    _name ="reservstion.hotels"
    _description ="reservstion.hotels"

    product_id =fields.Many2one('product.template',domain="[('book_type','=','hotel'),('is_booking_type','=',True)]")
    booking_start_date =  fields.Datetime(string='Check-in  Date' )
    booking_end_date =fields.Datetime(string='Check-out  Date' )
    
    list_price = fields.Float(string="Price",related='product_id.list_price')
    quantity = fields.Integer(string="Quantity" ,default=1)
    reservstion_id = fields.Many2one('travel_tour_agency.reservation', string="Reservation")
