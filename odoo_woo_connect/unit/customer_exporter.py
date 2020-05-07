# -*- coding: utf-8 -*-
#
#
#    Techspawn Solutions Pvt. Ltd.
#    Copyright (C) 2016-TODAY Techspawn(<http://www.Techspawn.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import logging
from ..model.api import API
from datetime import datetime
from datetime import timedelta
from backend_adapter import WpImportExport
_logger = logging.getLogger(__name__)


class WpCustomerExport(WpImportExport):

    """ Models for woocommerce customer export """

    def get_api_method(self, method, args):
        """ get api for customer"""
        api_method = None
        if method == 'customer':
            if not args[0]:
                api_method = 'customers'
            else:
                api_method = 'customers/' + str(args[0])
        return api_method

    def get_shipping_address(self, shipping_ids):
        """ return shipping address od customer """
        shipping = []
        if shipping_ids:
            for shipping_id in shipping_ids:
                shipping.append({
                    "first_name": shipping_id.ship_first_name or None,
                    "last_name": shipping_id.ship_last_name or None,
                    "address_1": shipping_id.ship_address1 or None,
                    "address_2": shipping_id.ship_address2 or None,
                    "city": shipping_id.ship_city or None,
                    "state": shipping_id.ship_state.code or None,
                    "postcode": shipping_id.ship_zip or None,
                    "country": shipping_id.ship_country.code or None,
                })
            return shipping[0]
        return shipping

    def export_customer(self, method, arguments):
        """ Export customer data"""
        _logger.debug("Start calling Woocommerce api %s", method)

        if arguments[1].company_type == 'company':
            company = arguments[1].name
        else:
            company = None

        result_dict = {
            "email": arguments[1].email or None,
            "first_name": arguments[1].first_name or arguments[1].name or None,
            "last_name": arguments[1].last_name or None,
            "username": arguments[1].username or None,
            "password": arguments[1].password or 'None',
            "company": company or None,
            "billing": {"first_name": arguments[1].first_name or arguments[1].name or None,
                        "last_name": arguments[1].last_name or None,
                        "company": arguments[1].company or None,
                        "address_1": arguments[1].street or None,
                        "address_2": arguments[1].street2 or None,
                        "city": arguments[1].city or None,
                        "state": arguments[1].state_id.code or None,
                        "postcode": arguments[1].zip or None,
                        "country": arguments[1].country_id.code or None,
                        "email": arguments[1].email or None,
                        "phone": arguments[1].phone or None,
                        },
            "shipping": self.get_shipping_address(arguments[1].shipping_ids),
        }

        r = self.export(method, result_dict, arguments)

        return {'status': r.status_code, 'data': r.json()}
