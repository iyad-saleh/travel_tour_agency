# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import  ValidationError
from datetime import datetime


class AirPort(models.Model):
    _name = 'travel_tour_agency.airport'
    _description = 'travel_tour_agency.airport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence,id'
    _rec_name="iata_code"

    
    airport_type  =fields.Selection([
                    ('large_airport', 'large_airport'),
                    ('meduim_airport', 'meduim_airport'),  ], default='large_airport', string="Type")
    name  = fields.Char(string="AirPort Name")#:Damascus International Airport
    elevation_ft = fields.Char(string="elevation_ft")#:2020
    continent = fields.Char(string="continent")#:AS
    iso_country = fields.Char(string="iso_country")#:SY
    iso_region = fields.Char(string="iso_region")#:SY-DI
    municipality = fields.Char(string="municipality")#:Damascus
    gps_code = fields.Char(string="gps_code")#:OSDI
    iata_code = fields.Char(string="IATA Code")#:DAM
    local_code = fields.Char(string="local_code")#
    coordinates = fields.Char(string="coordinates")# :"33.4114990234375, 36.51559829711914"
    sequence = fields.Integer(default=10,help="Gives the sequence order .")                                            # string="Flight Schedule")

class AirLine(models.Model):
    _name = 'travel_tour_agency.airline'
    _description = 'travel_tour_agency.airline.Company'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence,id'
    _rec_name = 'name'

    name = fields.Char(string="AirLine Company" , required=True)
    image = fields.Binary(string="AirLine Company Image")
    flight_ids = fields.One2many('travel_tour_agency.airline.flight', 'airline_id',
                                            string="AirLine Flights")
    sequence = fields.Integer(default=10,help="Gives the sequence order .")


    @api.model
    def create(self, vals):
        res= super(AirLine, self).create(vals)
        sl_no = 0
        for flight in res.flight_ids:
            sl_no +=1
            flight.sl_no =sl_no
        return res   
         
    def write(self, vals):
        res= super(AirLine, self).write(vals)
        sl_no = 0
        for flight in self.flight_ids:
            sl_no +=1
            flight.sl_no =sl_no
        return res  

class Flight(models.Model):
    _name        = 'travel_tour_agency.airline.flight'
    _description = 'travel_tour_agency.airline.flights'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence,id'
    _rec_name = 'name'

    flightNo    = fields.Char(string="Flight Number" ,required=True)
    airline_id  = fields.Many2one('travel_tour_agency.airline')
    image = fields.Binary(string="AirLine Company Image" ,related='airline_id.image')    
    flightschedule_ids = fields.One2many('travel_tour_agency.airline.flightschedule', 'flight_id',
                                            string="Flight Schedule")
    seat_ids = fields.One2many('travel_tour_agency.airline.flight.seat', 'flight_id',
                                            string="Flight Seats")
    sequence = fields.Integer(default=10,help="Gives the sequence order .")
    sl_no    = fields.Integer(string="SN")
    name = fields.Char(string='Name', compute='_compute_name_combination', store=True)
 

    @api.depends('flightNo', 'airline_id')
    def _compute_name_combination(self):
        for rec in self:
            rec.name = str(rec.airline_id.name) + '[' + str(rec.flightNo) +']'

    @api.model
    def create(self, vals):
        res= super(Flight, self).create(vals)
        sl_no = 0
        for schedule in res.flightschedule_ids:
            sl_no +=1
            schedule.sl_no =sl_no
        return res   
         
    def write(self, vals):
        res= super(Flight, self).write(vals)
        sl_no = 0
        for schedule in self.flightschedule_ids:
            sl_no +=1
            schedule.sl_no =sl_no
        return res  

class FlightSchedule(models.Model):
    _name        = 'travel_tour_agency.airline.flightschedule'
    _description = 'travel_tour_agency.airline.flightSchedule'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'sequence,departueDate'
    _rec_name    = 'name'

    airline_id    = fields.Many2one('travel_tour_agency.airline' , related='flight_id.airline_id')
    image         = fields.Binary(string="AirLine Company Image" , related='flight_id.airline_id.image')       
    flight_id     = fields.Many2one('travel_tour_agency.airline.flight', required=True)
    seat_ids       = fields.One2many('travel_tour_agency.airline.flight.seat', 'flight_id',
                                            string="Flight Seats" , related='flight_id.seat_ids')    
    
    origin        = fields.Many2one('travel_tour_agency.airport', string="Origin" , required=True)
    destination   = fields.Many2one('travel_tour_agency.airport', string="Destination" , required=True)
    departueDate  = fields.Datetime(string='Departue  Date' , required=True)
    arrivalDate   = fields.Datetime(string='Arrival  Date' , required=True)
    duration      = fields.Char(string='Duration', compute='_computDuration')
    remarks       = fields.Text(string="Nots")
    state         = fields.Selection([
                    ('scheduled', 'SCHEDULED'),
                    ('active', 'ACTIVE'),
                    ('delayed', 'DELAYED'),
                    ('departed', 'DEPARTED'),
                    ('canceled', 'CANCELLED')], default='scheduled', string="Status")
    sequence = fields.Integer(default=10,help="Gives the sequence order .")
    sl_no    = fields.Integer(string="SN")
    name = fields.Char(string='Name', compute='_compute_name_combination' , store=True)

    @api.constrains('departueDate','arrivalDate')
    def _check_date(self):
        for rec in self:
            if rec.departueDate < fields.datetime.now() or rec.departueDate > rec.arrivalDate:
                raise ValidationError(_("the entered date is not acceptable!!!"))            

    def _computDuration(self):
        t=[]
        for rec in self:
            diff = rec.arrivalDate - rec.departueDate
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            # seconds = seconds % 60
            if days:
                t.append(str(days)+'Day ') 
            t.append(str(hours)) 
            t.append(str(minutes)) 

            rec.duration =':'.join(t) 

    @api.depends('flight_id','state')
    def _compute_name_combination(self):
        for rec in self:
            rec.name = str(rec.flight_id.name) + '/' + str(rec.state)  

    def make_scheduled(self):
        for rec in self:
            rec.state = 'scheduled'

    def action_delayed(self):
        for rec in self:
            rec.state = 'delayed'
    
    def action_canceled(self):
        for rec in self:
            seats = self.env['travel_tour_agency.airline.flight.seat'].search([('flight_id','=', rec.flight_id.id)])
            for seat in seats:
                default_code= str(rec.flight_id.flightNo)+'/'+str(seat.seatClass)+'/'+str(rec.id)
                products =  self.env['product.template'].search([('default_code','ilike',default_code)])
                for product in products:
                    product.write({'active':False})   #toggle_active
            rec.state = 'canceled'



    def action_active(self):
        for rec in self:
            seats = self.env['travel_tour_agency.airline.flight.seat'].search([('flight_id','=', rec.flight_id.id)])
            products=[]
            for seat in seats:
                default_code= str(rec.flight_id.flightNo)+'/'+str(seat.seatClass)+'/'+str(rec.id)
                products =  self.env['product.template'].search([('default_code','ilike',default_code)])
                 
            if products:
                for product in products:
                    product.write({'active':True}) #toggle_active
            else:
                if not seats:
                    notification = {
                       'type': 'ir.actions.client',
                       'tag': 'display_notification',
                       'params': {
                           'title': _('Make Airline Service'),
                           'message': "You  can't make Airline Service without any Seat !!Add seat in flight ",
                           'sticky': (False),
                           }
                         }
                    return notification

                for seat in seats:
                    # default_code= str(rec.flight_id.flightNo)+'/'+str(seat.seatClass)+'/'+str(rec.id)
                    if seat.vendor:
                        supplier_info = self.env['product.supplierinfo'].create({
                        'name': seat.vendor.id,
                        'price': seat.cost,})
                    else :
                        partner = self.env['res.partner'].create({'name': rec.airline_id.name, 'email': 'from.test@airline.com'})
                        supplier_info = self.env['product.supplierinfo'].create({
                        'name': partner.id,
                        'price': seat.cost,})

                    self.env['product.template'].create({
                        'name': str(seat.name),
                        'list_price': seat.sell,
                        'standard_price': seat.cost,
                        'type': 'service',
                        'book_type':'airline',
                        'is_booking_type':True,
                        'origin':rec.origin.id   ,
                        'destination':rec.destination.id   ,
                        'booking_start_date': rec.departueDate,
                        'booking_end_date': rec.arrivalDate,
                        'image_1920':rec.image,
                        'active': True,# False,
                        'seller_ids': [(6, 0, [supplier_info.id])],
                        'default_code': str(rec.flight_id.flightNo)+'/'+str(seat.seatClass)+'/'+str(rec.id),
                        
                    })
            rec.state = 'active'


class Seat(models.Model):
    _name        = 'travel_tour_agency.airline.flight.seat'
    _description = 'travel_tour_agency.airline.flight.seat'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence,id'
    _rec_name    = 'name'

    flight_id     = fields.Many2one('travel_tour_agency.airline.flight')
    seatNo        = fields.Integer(string="Seats Number")
    seatClass     = fields.Selection([
                    ('economy', 'Economy Class'),
                    ('business', 'Business Class'),
                    ('first_class', 'First Class'),
                    ], default='economy', string="Class")
    cost              = fields.Float(string='cost price')
    sell              = fields.Float(string='sell price')    
    sequence = fields.Integer(default=10,help="Gives the sequence order .")
    sl_no    = fields.Integer(string="SN")
    name = fields.Char(string='Name', compute='_compute_name_combination', store=True)
    vendor= fields.Many2one('res.partner', string="Vendor") 

    
    @api.depends('flight_id','seatClass')
    def _compute_name_combination(self):
        for rec in self:
            rec.name = str(rec.flight_id.name) + '/' + str(rec.seatClass)  


