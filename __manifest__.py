# -*- coding: utf-8 -*-
{
    'name': "travel_tour_agency",

    'summary': """
        travel and tour agency managment system""",

    'description': """
        travel and tour agency managment system
    """,
    'sequence': 1,
    'author': "Iyad Ali Saleh",
    'website': "http://www.Travel.Tour.Agency.com",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'travel',
     'version': '15.0.0.1',
    'application':True,
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['base','mail','account','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/travel_tour_agency.airport.csv',
        'data/travel_tour_agency.airport.csv',
        'data/sequence_data.xml',
        'data/travel_tour_agency_airline_data.xml',
        'data/travel_tour_agency_hotel_data.xml',
        # 'data/travel_tour_agency_account_data.xml',
        'wizard/create_reservation_view.xml',
        'views/customer.xml',
        'views/passenger.xml',
        'views/airline.xml',
        'views/airport.xml',
        'views/country.xml',
        'views/flight.xml',
        'views/flightschedule.xml',
        'views/product.xml',
        'views/hotel.xml',
        'views/account.xml',
        'views/reservation.xml',
        'views/menu.xml',
        
    ],
}
