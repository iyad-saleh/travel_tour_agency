from datetime import date
from odoo import models, fields, api






class Passenger(models.Model):
    _name = 'travel_tour_agency.passenger'
    _description = 'travel_tour_agency.passenger'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    first_name         = fields.Char(string='First Name',required=True,  tracking=True)
    last_name          = fields.Char(string='Last Name', required=True, tracking=True)
    father_name        = fields.Char(string='Father Name', tracking=True)
    mother_name        = fields.Char(string='Mother Name', tracking=True)
    birth_date         =fields.Date(string='Birth Date'  )
    birth_place        = fields.Char(string='Birth Place', tracking=True)
    national_number    = fields.Char(string='National Number', tracking=True)
    nationality        = fields.Char(string='Nationality', tracking=True)
    gender             = fields.Selection( [('male','Male'),('female','Female')] ,string='Gender' )
    passport_number    = fields.Char(string='Passport Number')
    issue_date         =fields.Date(string='Issue Date'  )
    issue_end          =fields.Date(string='Issue End'  )
    issue_place        =fields.Char(string='Issue Place') 
    passport_image_ids = fields.One2many('travel_tour_agency.passport_image', 'passenger_id',
                                            string="Passport Images")
    partner_id = fields.Many2one('res.partner')
    name = fields.Char(string='Combination', compute='_compute_name_combination')


    @api.depends('first_name', 'last_name')
    def _compute_name_combination(self):
        for rec in self:
            rec.name = rec.first_name + ' ' + rec.last_name

class PassportImage(models.Model):
    _name = 'travel_tour_agency.passport_image'
    _description = 'travel_tour_agency.passport_image'

    image        = fields.Binary(string="Passport Image") 
    passenger_id = fields.Many2one('travel_tour_agency.passenger')
 

  