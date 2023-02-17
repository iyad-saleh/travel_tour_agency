# -*- coding: utf-8 -*-

from odoo import models, fields, api



class city(models.Model):
    _name = 'travel_tour_agency.city'
    _description = 'travel_tour_agency.city'
    # _parent ='country_id'
    # _parent_store =True
    _rec_name="name"


    name    = fields.Char(string="City")
    country_id = fields.Many2one(string="Country", comodel_name='res.country')
   



