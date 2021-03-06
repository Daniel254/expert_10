# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    Thinkopen - Portugal & Brasil
#    Copyright (C) Thinkopen Solutions (<http://www.thinkopensolutions.com>).
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
##############################################################################

{
    'name': 'Multiple Duplication',
    'version': '0.012.1',
    'category': 'Tools',
    'sequence': 38,
    'complexity': 'normal',
    'description': ''' This module allows to create multiple duplicate records in one go. ''',
    'author': 'ThinkOpen Solutions',
    'website': 'http://www.thinkopensolution.com',
    'images': ['images/oerp61.jpeg', ],
    'depends': [
        'base',
    ],
    'init_xml': [],
    'data': [
        'wizard/mulitiple_duplicate_view.xml',
        'views/multiple_duplicates_view.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'application': False,
    'certificate': '',
    'auto_install': False,
}
