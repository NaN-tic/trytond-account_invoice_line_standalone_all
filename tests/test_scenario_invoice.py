import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear,
                                                 get_accounts)
from trytond.modules.account_invoice.tests.tools import \
    set_fiscalyear_invoice_sequences
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Activate module
        activate_modules('account_invoice_line_standalone_all')

        # Create company
        _ = create_company()
        company = get_company()
        tax_identifier = company.party.identifiers.new()
        tax_identifier.type = 'eu_vat'
        tax_identifier.code = 'BE0897290877'
        company.party.save()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create party
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.save()

        # Create account category
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'service'
        template.list_price = Decimal('40')
        template.account_category = account_category
        template.save()
        product, = template.products

        # Create invoice
        Invoice = Model.get('account.invoice')
        InvoiceLine = Model.get('account.invoice.line')
        invoice = Invoice()
        invoice.party = party
        line1 = InvoiceLine()
        invoice.lines.append(line1)
        line1.product = product
        line1.quantity = 5
        line1.unit_price = Decimal('40')
        line2 = InvoiceLine()
        invoice.lines.append(line2)
        line2.account = revenue
        line2.description = 'Test'
        line2.quantity = 1
        line2.unit_price = Decimal(20)
        self.assertEqual(invoice.untaxed_amount, Decimal('220.00'))
        self.assertEqual(invoice.tax_amount, Decimal('0.00'))
        self.assertEqual(invoice.total_amount, Decimal('220.00'))
        invoice.save()
        line1, line2 = invoice.lines
        self.assertEqual(line1.party, party)
        self.assertEqual(line1.invoice_type, invoice.type)
        self.assertEqual(line2.party, party)
        self.assertEqual(line2.invoice_type, invoice.type)

        # Move first line to another invoice
        new_invoice = Invoice()
        new_invoice.party = party
        new_invoice.lines.append(InvoiceLine(line1.id))
        new_invoice.save()
        self.assertEqual(len(new_invoice.lines), 1)
        invoice.reload()
        self.assertEqual(len(invoice.lines), 1)

        # Post invoice
        invoice.click('post')
        self.assertEqual(invoice.state, 'posted')
        new_invoice.click('post')
        self.assertEqual(new_invoice.state, 'posted')
