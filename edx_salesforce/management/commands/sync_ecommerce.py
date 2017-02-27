from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = 'Synchronize the user account data for the given site/organization with a Salesforce account'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--site-domain',
            dest='site_domain',
            required=True,
            help='Domain of site for which user account data should be collected'
        )
        parser.add_argument(
            '-o',
            '--orgs',
            nargs='+',
            dest='orgs',
            required=True,
            help=(
                'Organizations for which user account data should be collected for '
                'course purchases associated with those organizations'
            )
        )

    def handle(self, *args, **options):
        site_domain = options['site_domain']
        orgs = options['orgs']

        self.stdout.write('Syncing user account data for site {site} and orgs {orgs}...'.format(
            site=site_domain,
            orgs=','.join(orgs)
        ))

        with connections['ecommerce'].cursor() as cursor:
            query = "Select ecommerce.order_order.date_placed, ecommerce.order_line.line_price_incl_tax," \
                    "ecommerce.catalogue_product.course_id, ecommerce.voucher_voucher.code " \
                    "from ecommerce.order_order " \
                    "Join ecommerce.order_line " \
                    "on ecommerce.order_line.order_id = ecommerce.order_order.id " \
                    "Join ecommerce.catalogue_product " \
                    "on ecommerce.catalogue_product.id = ecommerce.order_line.product_id " \
                    "Left Join ecommerce.basket_basket_vouchers " \
                    "on ecommerce.basket_basket_vouchers.basket_id = ecommerce.order_order.basket_id " \
                    "Left Join ecommerce.voucher_voucher " \
                    "on ecommerce.voucher_voucher.id = ecommerce.basket_basket_vouchers.voucher_id";

            cursor.execute(query)
            records = cursor.fetchall()
            print records
