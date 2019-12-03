# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    "name" : "Allow/Disable POS Features",
    "version" : "10.0.0.3",
    "category" : "Point of Sale",
    "depends" : ['base','sale','point_of_sale'],
    "price": 20,
    "currency": 'EUR',
    "author": "BrowseInfo",
    'summary': 'This apps helps to Allow and Disable POS Features like Payment, Qty, Discount, Edit Price, Remove Orderline',
    "description": """

    Purpose :-
    Allow/Deny POS Features like Payment, Qty, Discount, Edit Price, Remove Orderline for Particular POS User...!!!
    """,
    "website" : "www.browseinfo.in",
    "data": [
        'views/custom_pos_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_disable_payments.xml',
    ],
    "auto_install": False,
    "installable": True,
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
