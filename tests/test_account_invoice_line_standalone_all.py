# This file is part account_invoice_line_standalone_all module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown
from trytond.tests.test_tryton import doctest_checker
from trytond.tests.test_tryton import suite as test_suite


class AccountInvoiceLineStandaloneAllTestCase(ModuleTestCase):
    'Test Account Invoice Line Standalone All module'
    module = 'account_invoice_line_standalone_all'

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceLineStandaloneAllTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_invoice.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
