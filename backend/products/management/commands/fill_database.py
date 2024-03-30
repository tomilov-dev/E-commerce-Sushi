import sys
from pathlib import Path
from django.core.management.base import BaseCommand

ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from data.scraper import FarForScraper, BackupData
from data.add_data import JsonDataAdder, JsonDumpReader


class Command(BaseCommand):
    def data_added(self) -> bool:
        with open(ROOT_DIR / "backend" / "data_added.txt", "r") as file:
            added = file.read().strip()
            added = True if added == "True" else False
        return added

    def set_added(self) -> bool:
        with open(ROOT_DIR / "backend" / "data_added.txt", "w") as file:
            file.write("True")

    def handle(self, *args, **kwargs) -> None:
        if not self.data_added():
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

            self.set_added()
