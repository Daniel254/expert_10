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
import urllib2
import xmlrpclib
from collections import defaultdict
import base64
from odoo import models, fields, api, _
from ..unit.product_exporter import WpProductExport
from ..unit.product_tag_exporter import WpProductTagExport
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class ProductTags(models.Model):

    """ Models for product tags """
    _name = "product.product.tag"
    _order = 'sequence, name'

    sequence = fields.Integer('Sequence', help="Determine the display order")
    name = fields.Char(string="Name")
    slug = fields.Char(string="Slug")
    desc = fields.Text(string="Description")
    product_id = fields.Many2one(comodel_name='product.template',
                                 string='Product')
    backend_mapping = fields.One2many(comodel_name='wordpress.odoo.product.tag',
                                      string='Product tag mapping',
                                      inverse_name='product_tag_id',
                                      readonly=False,
                                      required=False,)
    backend_id = fields.Many2many(comodel_name='wordpress.configure',
                                  string='Woo Backend',
                                  store=True,
                                  readonly=False,
                                  required=True,
                                  )

    @api.model
    def create(self, vals):
        """ Override create method """
        backend_obj = self.env['wordpress.configure']
        backend_ids = backend_obj.search([('name', '!=', None)])
        vals['backend_id'] = [[6, 0, backend_ids.ids]]
        tag_id = super(ProductTags, self).create(vals)
        return tag_id

    @api.multi
    def sync_tag(self):
        for backend in self.backend_id:
            self.export_product_tag(backend)
        return

    @api.multi
    def export_product_tag(self, backend):
        """ export product attributes, save slug and create or update backend mapper """
        method = 'tag'
        mapper = self.backend_mapping.search(
            [('backend_id', '=', backend.id), ('product_tag_id', '=', self.id)])
        export = WpProductTagExport(backend)
        arguments = [mapper.woo_id or None, self]
        res = export.export_product_tag(method, arguments)
        if mapper and (res['status'] == 200 or res['status'] == 201):
            self.write({'slug': res['data']['slug']})
            mapper.write(
                {'product_tag_id': self.id, 'backend_id': backend.id, 'woo_id': res['data']['id']})
        elif (res['status'] == 200 or res['status'] == 201):
            self.write({'slug': res['data']['slug']})
            self.backend_mapping.create(
                {'product_tag_id': self.id, 'backend_id': backend.id, 'woo_id': res['data']['id']})


class ProductTagMapping(models.Model):

    """ Model to store woocommerce id for particular product"""
    _name = 'wordpress.odoo.product.tag'
    product_tag_id = fields.Many2one(comodel_name='product.product.tag',
                                     string='Product tag',
                                     ondelete='cascade',
                                     readonly=False,
                                     required=True,)

    backend_id = fields.Many2one(comodel_name='wordpress.configure',
                                 string='Backend',
                                 ondelete='set null',
                                 store=True,
                                 readonly=False,
                                 required=False,)

    woo_id = fields.Char(string='Woo id')


class ProductMultiImages(models.Model):

    """ Models for product images """
    _name = "product.multi.image"

    image = fields.Binary(string="Image")
    sequence = fields.Char(string="Seq")
    name = fields.Char(string="Name")
    default = fields.Boolean(string="Main Product Image")
    woo_id = fields.Char(string="Woo id")
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    position = fields.Integer(string="Position")
    src = fields.Char(string="Source")
    backend_mapping = fields.One2many(comodel_name='wordpress.odoo.product.image',
                                      string='Product Image mapping',
                                      inverse_name='product_image_id',
                                      readonly=False,
                                      required=False,)
    backend_id = fields.Many2many(comodel_name='wordpress.configure',
                                  string='Woo Backend',
                                  store=True,
                                  readonly=False,
                                  required=True,
                                  )


class ProductImageMapping(models.Model):

    """ Model to store woocommerce id for particular product"""
    _name = 'wordpress.odoo.product.image'
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product',
                                 ondelete='cascade',
                                 readonly=False,
                                 required=True,)
    product_image_id = fields.Many2one(comodel_name='product.multi.image',
                                       string='Product image',
                                       ondelete='cascade',
                                       readonly=False,
                                       required=True,)

    backend_id = fields.Many2one(comodel_name='wordpress.configure',
                                 string='Backend',
                                 ondelete='set null',
                                 store=True,
                                 readonly=False,
                                 required=False,)

    woo_id = fields.Char(string='Woo id')


class ProductTemplate(models.Model):

    """ Models for woocommerce product template """
    _inherit = 'product.template'

    website_published = fields.Boolean()
    from_wp = fields.Boolean('from_wp')
    # categ_id = fields.Many2one(string='Pricing/Primary Category')
    categ_ids = fields.Many2many(comodel_name='product.category',
                                 relation='product_categ_rel',
                                 column1='product_id',
                                 column2='categ_id',
                                 string='Product Categories')
    image_ids = fields.One2many(related='product_variant_ids.image_ids',
                                string='Product Images')
    tag_ids = fields.Many2many(comodel_name='product.product.tag',
                               inverse_name='product_id',
                               string='Product Tags')
    short_description = fields.Text('Short Description')
    slug = fields.Char('Slug')
    list_price = fields.Float('Final Sale Price')
    regular_price = fields.Float('Regular Price')
    sale_price = fields.Float('Sale Price')
    standard_price = fields.Float('Purchase Price')
    wp_managing_stock = fields.Boolean('WP Managing Stock')

    dimention_unit = fields.Many2one(comodel_name='product.uom',
                                     string='Dimention Unit',
                                     ondelete='set null')
    website_size_x = fields.Integer('Length')
    website_size_y = fields.Integer('Width')
    website_size_z = fields.Integer('Height')

    backend_mapping = fields.One2many(comodel_name='wordpress.odoo.product.template',
                                      string='Product mapping',
                                      inverse_name='product_id',
                                      readonly=False,
                                      required=False,
                                      )

    backend_id = fields.Many2many(comodel_name='wordpress.configure',
                                  string='Woo Backend',
                                  store=True,
                                  readonly=False,
                                  required=True,
                                  )

    @api.multi
    def wp_price_check(self, regular_price, sale_price, context=None):
        """ Check sales price and regular price """
        if sale_price > 0:
            list_price = sale_price
        else:
            list_price = regular_price

        if regular_price < sale_price:
            res = {'warning': {
                'title': _('Warning'),
                'message': _('Regular Price should be greater than Sale Price'),
            }
            }
            return res

        res = {'value': {
            'list_price': list_price,
            'regular_price': regular_price,
            'sale_price': sale_price,
        }
        }
        return res

    @api.model
    def create(self, vals):
        """ Override create method to check price before creating and export """
        if not 'regular_price' in vals.keys():
            vals['regular_price'] = 0
        if not 'sale_price' in vals.keys():
            vals['sale_price'] = 0
        check = self.wp_price_check(
            vals['regular_price'], vals['sale_price'], None)
        if 'warning' in check:
            raise Warning(check['warning']['message'])
        else:
            product_id = super(ProductTemplate, self).create(vals)
            return product_id

    @api.multi
    def write(self, vals):
        """ Override write method to export when any details is changed """
        if (self.backend_id or 'backend_id' in vals.keys()) and not ('default_code' in vals.keys() or 'slug' in vals.keys()):
            if not 'regular_price' in vals.keys():
                vals['regular_price'] = self.regular_price
            if not 'sale_price' in vals.keys():
                vals['sale_price'] = self.sale_price
            check = self.wp_price_check(
                vals['regular_price'], vals['sale_price'], None)
            if 'warning' in check:
                raise Warning(check['warning']['message'])
            else:
                vals.update(check['value'])
                product = super(ProductTemplate, self).write(vals)
                return product
        else:
            product = super(ProductTemplate, self).write(vals)
            return product

    @api.multi
    def sync_product(self):
        for backend in self.backend_id:
            self.export_product(backend)
        return

    @api.multi
    def export_product(self, backend):
        """ export product details, save default code & slug and create or update backend mapper """
        mapper = self.backend_mapping.search(
            [('backend_id', '=', backend.id), ('product_id', '=', self.id)])
        arguments = []
        method = 'products'
        arguments = [mapper.woo_id or None, self]
        export = WpProductExport(backend)
        res = export.export_product(method, arguments)
        if mapper and (res['status'] == 200 or res['status'] == 201):
            self.write(
                {'default_code': res['data']['sku'], 'slug': res['data']['slug']})
            mapper.write({'product_id': self.id, 'backend_id': backend.id, 'woo_id': res[
                         'data']['id'], 'image_id': res['data']['images'][0]['id']})
            self.map_product(res, backend)
        elif (res['status'] == 200 or res['status'] == 201):
            self.write(
                {'default_code': res['data']['sku'], 'slug': res['data']['slug']})
            self.backend_mapping.create({'product_id': self.id, 'backend_id': backend.id, 'woo_id': res[
                                        'data']['id'], 'image_id': res['data']['images'][0]['id']})
            self.map_product(res, backend)

    def map_product(self, res, backend):
        """ map product variants with particular woo id and create or update backend mapper"""
        if res['data']['variations']:
            for record in res['data']['variations']:
                variant_id = self.get_variations(
                    self.product_variant_ids, record, backend)
                mapper = variant_id.backend_mapping.search(
                    [('backend_id', '=', backend.id), ('product_id', '=', variant_id.id)])
                variant_id.write(
                    {'default_code': res['data']['sku'], 'slug': res['data']['slug']})
                if mapper:
                    mapper.write({'product_id': variant_id.id, 'backend_id': backend.id, 'woo_id': record[
                                 'id'], 'image_id': record['image'][0]['id']})
                else:
                    mapper.create({'product_id': variant_id.id, 'backend_id': backend.id, 'woo_id': record[
                        'id'], 'image_id': record['image'][0]['id']})

        return True

    def get_variations(self, variant_ids, record, backend):
        """ check and get the correct variant for particular woo id"""
        for variant_id in variant_ids:
            count = 0
            for attribute_value in variant_id.attribute_value_ids:
                for record_attr in record['attributes']:
                    if record_attr['option'] == attribute_value.name:
                        count += 1
                        if len(record['attributes']) == count:
                            return variant_id
                        else:
                            break


class ProductMapping(models.Model):

    """ Model to store woocommerce id for particular product"""
    _name = 'wordpress.odoo.product.template'

    product_id = fields.Many2one(comodel_name='product.template',
                                 string='Product Template',
                                 ondelete='cascade',
                                 readonly=False,
                                 required=True,
                                 )

    image_id = fields.Char('Image id')

    backend_id = fields.Many2one(comodel_name='wordpress.configure',
                                 string='Backend',
                                 ondelete='set null',
                                 store=True,
                                 readonly=False,
                                 required=False,
                                 )

    woo_id = fields.Char(string='Woo id')


class ProductProduct(models.Model):

    """ Models for woocommerce product variant """
    _inherit = 'product.product'

    woo_id = fields.Char(string='Woo id')
    image_ids = fields.One2many(comodel_name='product.multi.image',
                                inverse_name='product_id',
                                string='Product Images')
    regular_price = fields.Float('Regular Price')
    sale_price = fields.Float('Sale Price')
    lst_price = fields.Float('Final Sale Price')
    website_size_x = fields.Integer('Length')
    website_size_y = fields.Integer('Width')
    website_size_z = fields.Integer('Height')
    wp_managing_stock = fields.Boolean('WP Managing Stock')

    backend_mapping = fields.One2many(comodel_name='wordpress.odoo.product.product',
                                      string='Product mapping',
                                      inverse_name='product_id',
                                      readonly=False,
                                      required=False,
                                      )

    @api.model
    def create(self, vals):
        """ Override create method """
        return super(ProductProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        """ Override write method to export when any details is changed """
        return super(ProductProduct, self).write(vals)

    @api.multi
    def sync_product(self):
        for backend in self.product_tmpl_id.backend_id:
            self.product_tmpl_id.export_product(backend)
        return

    @api.multi
    def export_product(self, backend):
        """ export product variant details, and create or update backend mapper """
        return self.product_tmpl_id.export_product(backend)

    @api.multi
    def wp_price_check(self, regular_price, sale_price, context=None):
        """ Check sales price and regular price """
        if sale_price > 0:
            list_price = sale_price
        else:
            list_price = regular_price

        if regular_price < sale_price:
            res = {'warning': {
                'title': _('Warning'),
                'message': _('Regular Price should be greater than Sale Price'),
            }
            }
            return res

        res = {'value': {
            'regular_price': regular_price,
            'sale_price': sale_price,
        }
        }
        return res

    @api.multi
    def _website_price(self):
        try:
            res = super(ProductProduct, self)._website_price()
        except AttributeError:
            pass


class Website(models.Model):
    _inherit = "website"

    @api.model
    def get_current_website(self):
        try:
            res = super(Website, self).get_current_website()
        except RuntimeError:
            website_id = self._get_current_website_id('localhost')
            return self.browse(website_id)
        return res

    @api.multi
    def get_current_pricelist(self):
        try:
            res = super(Website, self).get_current_pricelist()
        except RuntimeError:
            return
        return res

    @api.multi
    def get_pricelist_available(self):
        try:
            res = super(Website, self).get_pricelist_available()
        except RuntimeError:
            return self.env['product.pricelist'].search([('id', '=', 1)]).id
        return res


class ProductProductMapping(models.Model):

    """ Model to store woocommerce id for particular product variant"""
    _name = 'wordpress.odoo.product.product'

    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product',
                                 ondelete='cascade',
                                 readonly=False,
                                 required=True,
                                 )

    image_id = fields.Char('Image id')

    backend_id = fields.Many2one(comodel_name='wordpress.configure',
                                 string='Backend',
                                 ondelete='set null',
                                 store=True,
                                 readonly=False,
                                 required=False,
                                 )

    woo_id = fields.Char(string='Woo id')


class StockInventory(models.TransientModel):

    """ Models for woocommerce product qty change"""
    _inherit = "stock.change.product.qty"

    wp_state = fields.Char('wp state')

    @api.multi
    def write(self, vals):
        """ Override write method to update the product qty"""
        if 'wp_state' in vals.keys():
            if vals['wp_state'] == 'done':
                self.change_product_qty()
        return super(StockInventory, self).write(vals)
