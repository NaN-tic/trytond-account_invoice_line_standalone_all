from trytond.pool import PoolMeta, Pool

__all__ = ['Line']


class Line(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @classmethod
    def create(cls, vlist):
        Invoice = Pool().get('account.invoice')

        invoices = Invoice.browse([x['invoice'] for x in vlist if
                x.get('invoice')])
        if invoices:
            # Store invoice type/party because accessing objects randomly could
            # be very inefficient due to cache invalidation
            cache = dict([(x.id, (x.type, x.party.id)) for x in invoices])
            vlist = vlist[:]
            for values in vlist:
                if values.get('invoice'):
                    if not values.get('invoice_type'):
                        values['invoice_type'] = cache[values['invoice']][0]
                    if not values.get('party'):
                        values['party'] = cache[values['invoice']][1]
        return super().create(vlist)
