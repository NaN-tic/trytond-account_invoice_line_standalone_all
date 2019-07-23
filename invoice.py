from trytond.pool import PoolMeta, Pool

__all__ = ['Line']


class Line(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @classmethod
    def create(cls, vlist):
        Invoice = Pool().get('account.invoice')

        invoices = Invoice.browse([x['invoice'] for x in vlist if 'invoice' in
                x])
        # Store invoice type/party because accessing objects randomly could be
        # very inefficient due to cache invalidation
        cache = dict([(x.id, (x.type, x.party.id)) for x in invoices])
        if cache:
            vlist = vlist[:]
            for values in vlist:
                if 'invoice' in values:
                    if not 'invoice_type' in values:
                        values['invoice_type'] = cache[values['invoice']][0]
                    if not 'party' in values:
                        values['party'] = cache[values['invoice']][1]
        return super().create(vlist)
