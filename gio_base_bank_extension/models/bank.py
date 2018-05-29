# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG
# Autor: Stéphane Diez
# Version: 1.0 - 29.05.2018

import re
from odoo import models, fields, api, _
from odoo.tools import mod10r
from odoo import exceptions

from odoo.addons.base_iban.models.res_partner_bank import normalize_iban

class BankCommon(object):

    def is_swiss_postal_num(self, number):
        return (self._check_9_pos_postal_num(number) or
                self._check_5_pos_postal_num(number))

    def _check_9_pos_postal_num(self, number):
        """
        Predicate that checks if a postal number
        is in format xx-xxxxxx-x is correct,
        return true if it matches the pattern
        and if check sum mod10 is ok
        :param number: postal number to validate
        :returns: True if is it a 9 len postal account
        :rtype: bool
        """
        pattern = r'^[0-9]{2}-[0-9]{1,6}-[0-9]$'
        if not re.search(pattern, number):
            return False
        nums = number.split('-')
        prefix = nums[0]
        num = nums[1].rjust(6, '0')
        checksum = nums[2]
        expected_checksum = mod10r(prefix + num)[-1]
        return expected_checksum == checksum

    def _check_5_pos_postal_num(self, number):
        """
        Predicate that checks if a postal number
        is in format xxxxx is correct,
        return true if it matches the pattern
        and if check sum mod10 is ok
        :param number: postal number to validate
        :returns: True if is it a 5 len postal account
        :rtype: bool
        """
        pattern = r'^[0-9]{1,5}$'
        if not re.search(pattern, number):
            return False
        return True

    def _convert_iban_to_ccp(self, iban):
        """
        Convert a Postfinance IBAN into an old postal number
        """
        iban = normalize_iban(iban)
        if not iban[:2].upper() == 'CH':
            return False
        part1 = iban[-9:-7]
        part2 = iban[-7:-1].lstrip('0')
        part3 = iban[-1:].lstrip('0')
        ccp = '{}-{}-{}'.format(part1, part2, part3)
        if not self._check_9_pos_postal_num(ccp):
            return False
        return ccp

    def _convert_iban_to_clearing(self, iban):
        """
        Convert a Swiss Iban to a clearing
        """
        iban = normalize_iban(iban)
        if not iban[:2].upper() == 'CH':
            return False
        clearing = iban[4:9].lstrip('0')
        return clearing


class ResPartnerBank(models.Model, BankCommon):
    _inherit = 'res.partner.bank'

    @api.depends('acc_number')
    def _compute_acc_type(self):
        todo = self.env['res.partner.bank']
        for rec in self:
            if (rec.acc_number and
                    rec.is_swiss_postal_num(rec.acc_number)):
                rec.acc_type = 'postal'
                continue
            todo |= rec
        super(ResPartnerBank, todo)._compute_acc_type()