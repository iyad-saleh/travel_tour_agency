from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_booking_type = fields.Boolean(string="Booking Product", default=False)
    book_type = fields.Selection([
        ('hotel', 'Hotel'),
        ('airline', 'Airline'),
        ('visa', 'Visa'),
         ], default='airline', string="Book Type")
    booking_start_date =  fields.Datetime(string='Start  Date' )
    booking_end_date =fields.Datetime(string='End  Date' )
    origin        = fields.Many2one('travel_tour_agency.airport', string="Origin" )
    destination   = fields.Many2one('travel_tour_agency.airport', string="Destination" )
    country_id = fields.Many2one(string="Country", comodel_name='res.country')
    city_id = fields.Many2one('travel_tour_agency.city', string="City")  
                        

class ProductProduct(models.Model):
    _inherit = "product.product"

    
    is_booking_type = fields.Boolean(string="Booking Product", default=False)
    book_type = fields.Selection([
        ('hotel', 'Hotel'),
        ('airline', 'Airline'),
        ('visa', 'Visa'),
         ], default='airline', string="Book Type")
    booking_start_date =  fields.Datetime(string='Start  Date' )
    booking_end_date =fields.Datetime(string='End  Date' )
    origin        = fields.Many2one('travel_tour_agency.airport', string="Origin" )
    destination   = fields.Many2one('travel_tour_agency.airport', string="Destination" )
    country_id = fields.Many2one(string="Country", comodel_name='res.country')
    city_id = fields.Many2one('travel_tour_agency.city', string="City") 