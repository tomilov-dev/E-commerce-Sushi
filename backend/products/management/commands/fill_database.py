import sys
from pathlib import Path
from django.core.management.base import BaseCommand

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from data.scraper import FarForScraper, BackupData
from data.add_data import JsonDataAdder, JsonDumpReader
from products.models import Product


class Command(BaseCommand):
    def data_added(self) -> bool:
        products = Product.objects.all()
        if len(products) >= 3:
            return True
        return False

    def handle(self, *args, **kwargs) -> None:
        if not self.data_added():
            print("Start Data Initialization")
            scraper = FarForScraper()
            backuper = BackupData()

            promos, categories = scraper.scrape()

            backuper.dump_promos(
                backuper.transfer_promos(promos),
            )
            backuper.dump_categories(
                backuper.transfer_categories(categories),
            )

            reader = JsonDumpReader()
            adder = JsonDataAdder()

            promos, categories = reader.read_all()

            adder.add_promos(promos)
            adder.add_products_data(categories)

        print("Data Initialized")
