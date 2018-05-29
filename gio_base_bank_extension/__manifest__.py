# -*- coding: utf-8 -*-
{
    'name': "gio_base_bank_extension",

    'summary': """
        Fixes a bug in l10n_ch_base_bank""",

    'description': """
        Fixes a bug in l10n_ch_base_bank
    """,

    'author': "giordano.ch AG",
    'website': "http://www.giordano.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '11.0.1.0',

    # any module necessary for this one to work correctly
     'depends': ['account_payment_partner', 'base_iban', 'l10n_ch_base_bank']
}
