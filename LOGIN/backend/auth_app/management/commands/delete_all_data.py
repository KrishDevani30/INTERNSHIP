from django.core.management.base import BaseCommand
from django.db import transaction
from auth_app.models import CustomUser, Order, OrderItem, OrderStatusHistory, DeleteLog, Product
import os
import shutil

class Command(BaseCommand):
    help = 'Deletes all users and related data from the system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion without confirmation',
        )

    def handle(self, *args, **options):
        if not options['force']:
            confirm = input('''
WARNING: This will delete ALL users and related data including:
- All users
- All orders
- All order items
- All order history
- All products
- All JSON order files

This action cannot be undone. Are you sure you want to continue? (yes/no): ''')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        try:
            with transaction.atomic():
                # Delete all order related data
                OrderStatusHistory.objects.all().delete()
                OrderItem.objects.all().delete()
                Order.objects.all().delete()
                
                # Delete all products
                Product.objects.all().delete()
                
                # Delete all users except superuser
                CustomUser.objects.filter(is_superuser=False).delete()
                
                # Delete all delete logs
                DeleteLog.objects.all().delete()

                # Delete all JSON order files
                json_dirs = [
                    os.path.join('SHOP', 'orders'),
                    os.path.join('LOGIN', 'frontend', 'orders')
                ]
                
                for dir_path in json_dirs:
                    if os.path.exists(dir_path):
                        for file in os.listdir(dir_path):
                            if file.endswith('.json'):
                                os.remove(os.path.join(dir_path, file))

            self.stdout.write(self.style.SUCCESS('Successfully deleted all data.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}')) 