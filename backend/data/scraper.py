import re
import os
import sys
import json
import random
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup as soup

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from data.models_dto import (
    TagDTO,
    UnitDTO,
    PromoDTO,
    ProductDTO,
    CategoryDTO,
    CharacteristicsDTO,
)

current_date = str(datetime.now().date())


BACKUP_DATA_PATH = Path(__file__).parent / "backup_data"
JSON_DUMP_PATH = BACKUP_DATA_PATH / "json_dump"

if not os.path.exists(BACKUP_DATA_PATH):
    os.mkdir(BACKUP_DATA_PATH)

if not os.path.exists(JSON_DUMP_PATH):
    os.mkdir(JSON_DUMP_PATH)


IMAGE_PATH = BACKUP_DATA_PATH / "images"
DUMP_PATH = JSON_DUMP_PATH / current_date


if not os.path.exists(DUMP_PATH):
    os.mkdir(DUMP_PATH)

if not os.path.exists(IMAGE_PATH):
    os.mkdir(IMAGE_PATH)


class Parsed(object):
    image_path: str = ""

    def _get_filename(
        self,
        url: str,
        object_name: str,
        counter: int = None,
    ) -> str:
        ext = "." + url.split(".")[-1]

        if counter is None:
            counter = ""
        elif counter is not None:
            counter = str(counter)

        return object_name + counter + ext

    def save_image(
        self,
        url: str,
        object_name: str,
        duplicates=False,
    ) -> None:
        image = requests.get(url)

        filename = self._get_filename(url, object_name)
        path = IMAGE_PATH / filename

        if duplicates:
            if os.path.exists(path):
                self.image = path

            else:
                with open(path, "wb") as file:
                    file.write(image.content)

        else:
            counter = 1
            while os.path.exists(path):
                filename = self._get_filename(url, object_name, counter)
                path = IMAGE_PATH / filename
                counter += 1

            with open(path, "wb") as file:
                file.write(image.content)

        self.image_path = filename


class Tag(Parsed):
    def __init__(
        self,
        name: str,
        image_url: str,
    ) -> None:
        self.name = name
        self.image_url = image_url

        self.save_image(
            self.image_url,
            "tag_" + self.name.replace(" ", "_"),
            True,
        )

    def __repr__(self) -> str:
        return f"""
--- Tag ---:
name: {self.name}
image_url: {self.image_url}
image_path: {self.image_path}
--- End Tag ---
"""


class Characteristics(object):
    def __init__(
        self,
        measure: str,
        measure_symbol: str,
        measure_count: str,
        quantity: int,
        proteins: int = None,
        fats: int = None,
        carbohydrates: int = None,
        kilocalories: int = None,
    ) -> None:
        self.measure = measure
        self.measure_symbol = measure_symbol
        self.measure_count = measure_count
        self.quantity = quantity

        self.proteins = proteins
        self.fats = fats
        self.carbohydrates = carbohydrates
        self.kilocalories = kilocalories

    def add_extra_data(
        self,
        proteins: int = None,
        fats: int = None,
        carbohydrates: int = None,
        kilocalories: int = None,
    ) -> None:
        mc = self.measure_count / 100
        if proteins:
            self.proteins = int(mc * proteins)
        if fats:
            self.fats = int(mc * fats)
        if carbohydrates:
            self.carbohydrates = int(mc * carbohydrates)
        if kilocalories:
            self.kilocalories = int(mc * kilocalories)

    def __repr__(self):
        return f"""
Characteristics:
measure: {self.measure}
measure_symbol: {self.measure_symbol}
measure_count: {self.measure_count}
quantity: {self.quantity}
proteins: {self.proteins}
fats: {self.fats}
carbohydrates: {self.carbohydrates}
kilocalories: {self.kilocalories}
"""


class Unit(object):
    def __init__(
        self,
        name: str,
        price: str,
        measure: str,
        measure_symbol: str,
        measure_count: str,
        quantity: int,
        kf: int,
    ) -> None:
        self.name = name
        self.price = int(self.parse_int(price) * kf)
        self.discount_price = self.set_discount(kf)

        measure_count = int(self.parse_int(measure_count) * kf)
        self.characteristics = Characteristics(
            measure,
            measure_symbol,
            measure_count,
            quantity,
        )

    def parse_int(self, value: str | None) -> int | None:
        if value:
            return int(re.findall("\d+", value)[0])
        return None

    def set_discount(self, kf: float) -> int:
        if random.random() > 0.75:
            if random.random() < 0.75:
                return int(self.price * 0.80 * kf)

    def __repr__(self) -> str:
        return f"""
--- Unit ---
name: {self.name}
price: {self.price}
discount_price: {self.discount_price}
{self.characteristics}
--- End Unit ---
"""


class Product(Parsed):
    def __init__(
        self,
        url: str,
        name: str,
        description: str,
        image_url: str,
        tags: list[Tag],
        units: list[Unit],
    ) -> None:
        self.url = url
        self.name = name
        self.description = description
        self.image_url = image_url
        self.tags = tags

        self.units = units

        self.save_image(
            self.image_url,
            "product_" + self.name.replace(" ", "_"),
        )

    def __repr__(self) -> str:
        return f"""
Product:
name: {self.name}
description: {self.description}
image_url: {self.image_url}
image_path: {self.image_path}
tags: {self.tags}
units: {self.units}
"""


class Category(Parsed):
    def __init__(
        self,
        name: str,
        image_url: str,
        products: list[Product] = [],
    ) -> None:
        self.name = name
        self.image_url = image_url
        self.products = products

        self.save_image(
            self.image_url,
            "category_" + self.name.replace(" ", "_"),
        )

    def __repr__(self) -> str:
        return f"""
--- Category ---:
name: {self.name}
image_url: {self.image_url}
image_path: {self.image_path}
products: {self.products}
--- End Category ---
"""


class Promo(Parsed):
    def __init__(
        self,
        name: str,
        image_url: str,
        description: str,
    ) -> None:
        self.name = name
        self.image_url = image_url
        self.description = description

        self.save_image(
            self.image_url,
            "promo_" + self.name.replace(" ", "_"),
        )

    def __repr__(self) -> str:
        return f"""
--- Promo ---
name: {self.name}
image_url: {self.image_url}
image_path: {self.image_path}
description: {self.description}
--- End Promo ---
"""


class UnitData(object):
    def __init__(
        self,
        symb: str,
        quantity: int,
        kf: float = 1.0,
    ) -> None:
        self.symb = symb
        self.quantity = quantity
        self.kf = kf


class InputData(object):
    def __init__(
        self,
        url: str,
        measure: str,
        measure_symbol: str,
        units_data: list[UnitData],
    ) -> None:
        self.url = url
        self.measure = measure
        self.measure_symbol = measure_symbol
        self.units_data = units_data


class FarForScraper(object):
    """farfor.ru data"""

    main_url = "https://pervouralsk.farfor.ru"

    input_data = [
        InputData(
            "https://pervouralsk.farfor.ru/category/rolly/",
            "Грамм",
            "г",
            [UnitData("8 шт", 8, 1), UnitData("4 шт", 4, 0.7)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/sety/",
            "Грамм",
            "г",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/pizza/",
            "Грамм",
            "г",
            [UnitData("25 см", 1, 0.7), UnitData("30 см", 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/wok/",
            "Грамм",
            "г",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/zakuski/",
            "Грамм",
            "г",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/supy/",
            "Миллилитр",
            "мл",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/salaty/",
            "Грамм",
            "г",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/dessert/",
            "Грамм",
            "г",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/dobawky/",
            "Грамм",
            "г",
            [UnitData(None, 1, 1)],
        ),
        InputData(
            "https://pervouralsk.farfor.ru/category/napitki/",
            "Миллилитр",
            "мл",
            [UnitData(None, 1, 1)],
        ),
    ]

    def _parse_tags(self, tag_element: soup) -> list[Tag]:
        tags = []

        stags = tag_element.find_all("img")
        for stag in stags:
            name = stag.get("alt")
            img = stag.get("src")

            tag = Tag(name, img)
            tags.append(tag)

        return tags

    def _parse_products(
        self,
        html: str,
        measure: str,
        input_data: InputData,
    ) -> list[Product]:
        s = soup(html, "lxml")
        catlist = s.find("div", {"class": "category__list-desktop"})
        sproducts = catlist.find_all("div", "product")

        products: list[Product] = []
        for sproduct in sproducts:
            img = sproduct.find("a", {"class": "product__image"}).find("img").get("src")
            content = sproduct.find("div", {"class": "product__content"})
            title = content.find("a", {"class": "product__content-title"}).text
            url = self.main_url + content.find(
                "a", {"class": "product__content-title"}
            ).get("href")
            description = content.find(
                "a", {"class": "product__content-description"}
            ).text
            price = content.find("div", {"class": "product__content-price"}).text
            measure_count = content.find(
                "div", {"class": "product__content-weight"}
            ).text.replace("гКБЖУ", "")

            tags_element = sproduct.find("div", {"class": "product__tags"})
            tags = self._parse_tags(tags_element)

            units_data: list[UnitData] = input_data.units_data

            units: list[Unit] = []
            for ud in units_data:
                unit = Unit(
                    ud.symb,
                    price,
                    measure,
                    input_data.measure_symbol,
                    measure_count,
                    ud.quantity,
                    ud.kf,
                )
                units.append(unit)

            product = Product(
                url=url,
                name=title,
                description=description,
                image_url=img,
                tags=tags,
                units=units,
            )

            products.append(product)

        return products

    def _parse_category(self, html: str) -> Category:
        s = soup(html, "lxml")
        catbar = s.find("div", {"class": "v-slide-group__content"})
        cat = catbar.find("a", {"class": "router-link-active"})

        name = cat.text
        img = cat.find("img").get("src")

        return Category(
            name=name,
            image_url=img,
        )

    def _add_extra_info(
        self,
        product: Product,
    ) -> None:
        html = requests.get(product.url).text

        s = soup(html, "lxml")
        tab = s.find("div", {"class": "product__content-calories"})
        cols = tab.find_all("th")

        data = []
        if cols and len(cols) > 0:
            for col in cols[1:]:
                val = int(re.search("\d+", col.text)[0])
                data.append(val)

        while len(data) < 4:
            data.append(None)

        for unit in product.units:
            charchs = unit.characteristics
            charchs.add_extra_data(*data)

    def _parse_promos(self, html: str) -> list[Promo]:
        s = soup(html, "lxml")
        sales_list = s.find("div", {"class": "sales__grid"})
        ssales = sales_list.find_all("div", {"class": "sale__item"})

        sales: list[Promo] = []
        for ssale in ssales:
            top = ssale.find("a", {"class": "sale__top"})

            name = top.text
            img = top.find("img").get("src")
            description = ssale.find("div", {"class": "sale__bottom-description"}).text

            sale = Promo(
                name=name,
                image_url=img,
                description=description,
            )
            sales.append(sale)

        return sales

    def _get_promos(self) -> list[Promo]:
        URL = self.main_url + "/sales/"
        html = requests.get(URL).text

        sales = self._parse_promos(html)
        return sales

    def scrape(self) -> tuple[list[Promo], list[Category]]:
        categories: list[Category] = []

        for inp in self.input_data:
            category_url = inp.url
            measure = inp.measure

            html = requests.get(category_url).text

            category = self._parse_category(html)
            products = self._parse_products(html, measure, inp)

            for product in products:
                self._add_extra_info(product)

            category.products = products
            categories.append(category)

        promos = self._get_promos()
        return promos, categories


class BackupData(object):
    def transfer_promos(
        self,
        promos: list[Promo],
    ) -> list[PromoDTO]:
        promos_dtos = []
        for promo in promos:
            promo_dto = PromoDTO(
                image_url=promo.image_url,
                image_path=promo.image_path,
                name=promo.name,
                description=promo.description,
                id=None,
            )
            promos_dtos.append(promo_dto)

        return promos_dtos

    def transfer_characteristics(
        self,
        charachteristics: Characteristics,
    ) -> CharacteristicsDTO:
        return CharacteristicsDTO(
            measure=charachteristics.measure,
            measure_symbol=charachteristics.measure_symbol,
            measure_count=charachteristics.measure_count,
            quantity=charachteristics.quantity,
            proteins=charachteristics.proteins,
            fats=charachteristics.fats,
            carbohydrates=charachteristics.carbohydrates,
            kilocalories=charachteristics.kilocalories,
            id=None,
        )

    def transfer_units(
        self,
        units: list[Unit],
    ) -> list[UnitDTO]:
        units_dtos: list[UnitDTO] = []
        for unit in units:
            charchs = unit.characteristics
            charchs_dto = self.transfer_characteristics(charchs)

            unit_dto = UnitDTO(
                name=unit.name,
                price=unit.price,
                discount_price=unit.discount_price,
                characteristics=charchs_dto,
                id=None,
            )

            units_dtos.append(unit_dto)

        return units_dtos

    def transfet_tags(
        self,
        tags: list[Tag],
    ) -> list[Tag]:
        tags_dtos: list[TagDTO] = []
        for tag in tags:
            tag_dto = TagDTO(
                image_url=tag.image_url,
                image_path=tag.image_path,
                name=tag.name,
                id=None,
            )

            tags_dtos.append(tag_dto)

        return tags_dtos

    def transfer_products(
        self,
        products: list[Product],
    ) -> list[ProductDTO]:
        products_dtos: list[ProductDTO] = []
        for product in products:
            tags = product.tags
            units = product.units

            units_dtos = self.transfer_units(units)
            tags_dtos = self.transfet_tags(tags)

            product_dto = ProductDTO(
                image_url=product.image_url,
                image_path=product.image_path,
                name=product.name,
                description=product.description,
                tags=tags_dtos,
                units=units_dtos,
                id=None,
            )

            products_dtos.append(product_dto)

        return products_dtos

    def transfer_categories(
        self,
        categories: list[Category],
    ) -> list[CategoryDTO]:
        categories_dtos: list[CategoryDTO] = []
        for category in categories:
            products: list[Product] = category.products
            products_dtos = self.transfer_products(products)

            category_dto = CategoryDTO(
                image_url=category.image_url,
                image_path=category.image_path,
                name=category.name,
                products=products_dtos,
                id=None,
            )
            categories_dtos.append(category_dto)

        return categories_dtos

    def dump_categories(self, categories: list[CategoryDTO]) -> None:
        for index in range(len(categories)):
            category = categories[index]
            data = category.model_dump()

            if not os.path.exists(DUMP_PATH):
                os.mkdir(DUMP_PATH)

            with open(DUMP_PATH / f"category_{index}.json", "w") as file:
                json.dump(data, file, ensure_ascii=False)

    def dump_promos(self, promos: list[PromoDTO]) -> None:
        for index in range(len(promos)):
            promo = promos[index]
            data = promo.model_dump()

            if not os.path.exists(DUMP_PATH):
                os.mkdir(DUMP_PATH)

            with open(DUMP_PATH / f"promo_{index}.json", "w") as file:
                json.dump(data, file, ensure_ascii=False)


if __name__ == "__main__":
    scraper = FarForScraper()
    backuper = BackupData()

    promos, categories = scraper.scrape()

    backuper.dump_promos(
        backuper.transfer_promos(promos),
    )
    backuper.dump_categories(
        backuper.transfer_categories(categories),
    )
