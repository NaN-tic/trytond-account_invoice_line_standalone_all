================
Invoice Scenario
================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax, create_tax_code
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences
    >>> today = datetime.date.today()

Activate module::

    >>> config = activate_modules('account_invoice_line_standalone_all')

Create company::

    >>> _ = create_company()
    >>> company = get_company()
    >>> tax_identifier = company.party.identifiers.new()
    >>> tax_identifier.type = 'eu_vat'
    >>> tax_identifier.code = 'BE0897290877'
    >>> company.party.save()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]
    >>> period_ids = [p.id for p in fiscalyear.periods]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> account_tax = accounts['tax']
    >>> account_cash = accounts['cash']

Create party::

    >>> Party = Model.get('party.party')
    >>> party = Party(name='Party')
    >>> party.save()

Create account category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'service'
    >>> template.list_price = Decimal('40')
    >>> template.account_category = account_category
    >>> template.save()
    >>> product, = template.products

Create invoice::

    >>> Invoice = Model.get('account.invoice')
    >>> InvoiceLine = Model.get('account.invoice.line')
    >>> invoice = Invoice()
    >>> invoice.party = party
    >>> line1 = InvoiceLine()
    >>> invoice.lines.append(line1)
    >>> line1.product = product
    >>> line1.quantity = 5
    >>> line1.unit_price = Decimal('40')
    >>> line2 = InvoiceLine()
    >>> invoice.lines.append(line2)
    >>> line2.account = revenue
    >>> line2.description = 'Test'
    >>> line2.quantity = 1
    >>> line2.unit_price = Decimal(20)
    >>> invoice.untaxed_amount
    Decimal('220.00')
    >>> invoice.tax_amount
    Decimal('0.00')
    >>> invoice.total_amount
    Decimal('220.00')
    >>> invoice.save()
    >>> line1, line2 = invoice.lines
    >>> line1.party == party
    True
    >>> line1.invoice_type == invoice.type
    True
    >>> line2.party == party
    True
    >>> line2.invoice_type == invoice.type
    True

Move first line to another invoice::

   >>> new_invoice = Invoice()
   >>> new_invoice.party = party
   >>> new_invoice.lines.append(InvoiceLine(line1.id))
   >>> new_invoice.save()
   >>> len(new_invoice.lines)
   1
   >>> invoice.reload()
   >>> len(invoice.lines)
   1

Post invoice::

    >>> invoice.click('post')
    >>> invoice.state
    'posted'
    >>> new_invoice.click('post')
    >>> new_invoice.state
    'posted'
