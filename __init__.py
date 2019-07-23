# This file is part account_invoice_line_standalone_all module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice

def register():
    Pool.register(
        invoice.Line,
        module='account_invoice_line_standalone_all', type_='model')
