from odoo import api, fields, models, _


# class AccountMove(models.Model):
#     _inherit = 'account.move'



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


    start_date = fields.Datetime(string="Start")
    end_date = fields.Datetime(string="End")
     


class AccountMoveLine(models.Model):
    _inherit = "account.move" 
    
    pnr= fields.Char(string="PNR")   
    passenger_ids = fields.Many2many('travel_tour_agency.passenger' )
    reservation_id = fields.Many2one('travel_tour_agency.reservation', string="Reservation " ,readonly=True)       