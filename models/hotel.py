# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class Hotel(models.Model):
    _name = 'travel_tour_agency.hotel'
    _description = 'travel_tour_agency.hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence,hotel_star'
    _rec_name="name"
    
    name = fields.Char(string="Hotel Name")
    hotel_star = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'), ], default='3', string="Stars")
    image = fields.Binary(string="Hotel Image")
    hotel_room_ids  = fields.One2many('travel_tour_agency.hotel.room', 'hotel_id',
                                            string="Rooms")
    country_id = fields.Many2one(string="Country", comodel_name='res.country')
    city_id = fields.Many2one('travel_tour_agency.city', string="City" ,
                         domain="[('country_id', '=', country_id)]")
    remarks  = fields.Text(string="Nots")
    address = fields.Text(string="Address")
    vendor= fields.Many2one('res.partner', string="Vendor")
    sequence = fields.Integer(default=10,help="Gives the sequence order .")
    state         = fields.Selection([
                    ('active', 'ACTIVE'),
                    ('deactive', 'DEACTIVE')], default='deactive', string="Status")



    def action_deactive(self):
        for rec in self:
            rooms = self.env['travel_tour_agency.hotel.room'].search([('hotel_id','=', rec.id)]) 

            for room in rooms:
                default_code =  str(rec.name)+'/'+str(room.name)+'/'+str(room.id)
                products =  self.env['product.template'].search([('default_code','=',default_code)])
                for product in products:
                    product.write({'active':False})
            rec.state = 'deactive'


    def action_active(self):

        for rec in self:
            rooms = self.env['travel_tour_agency.hotel.room'].search([('hotel_id','=', rec.id)]) 
            if not rooms:
                notification = {
                   'type': 'ir.actions.client',
                   'tag': 'display_notification',
                   'params': {
                       'title': _('Make Service'),
                       'message': "You  can't make Service without any Room !! Add Rooms ",
                       'sticky': (False),
                       }
                     }
                return notification
            for room in rooms:

                default_code =  str(rec.name)+'/'+str(room.name)+'/'+str(room.id)
              
                if room.vendor:
                    supplier_info = self.env['product.supplierinfo'].create({
                    'name': room.vendor.id,
                    'price': room.cost,})
                else :
                    partner = self.env['res.partner'].create({'name': rec.name, 'email': 'from.test@example.com'})
                    supplier_info = self.env['product.supplierinfo'].create({
                    'name': partner.id,
                    'price': room.cost,})

                self.env['product.template'].create({
                    'name': 'Hotel-'+str(rec.name)+'['+str(room.name)+']',
                    'list_price': room.sell,
                    'standard_price': room.cost,
                    'type': 'service',
                    'book_type':'hotel',
                    'country_id':rec.country_id.id,
                    'city_id':rec.city_id.id,
                    'is_booking_type':True,
                    'image_1920':rec.image,
                    'active': True,
                    'seller_ids': [(6, 0, [supplier_info.id])],
                    'default_code': default_code
                    
                })
            rec.state = 'active'
 


class HotelRoom(models.Model):
    _name = "travel_tour_agency.hotel.room"
    _description = "Hotel Room"
    _order = 'sequence,id'
    _rec_name="name"

    name = fields.Char(string="Room", required=True)
    description= fields.Text(string="description")
    cost = fields.Float(string='cost price')
    sell = fields.Float(string='sell price')
    hotel_id = fields.Many2one('travel_tour_agency.hotel')
    image = fields.Binary(string="Hotel Image" ,related="hotel_id.image")
    country_id = fields.Many2one('travel_tour_agency.country', string="Country", related="hotel_id.country_id" )
    city_id = fields.Many2one('travel_tour_agency.city', string="City", related="hotel_id.city_id" )
    vendor   = fields.Many2one('res.partner', string="Vendor", related="hotel_id.vendor" )
    sequence = fields.Integer(default=10,help="Gives the sequence order .")

