import logging
from django.core.management import BaseCommand, CommandError
from django.db import connections

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'empty help'

    def handle(self, *args, **options):
        cursor_edxapp = connections['default'].cursor()
        cursor_ecommerce = connections['ecomm'].cursor()

        cursor_edxapp.execute("SELECT * FROM auth_user")
        results = cursor_edxapp.fetchall()
        print results[0]

        print

        cursor_ecommerce.execute("SELECT * FROM ecommerce_user")
        results = cursor_ecommerce.fetchall()
        print results[0]

        print ("Hello world")