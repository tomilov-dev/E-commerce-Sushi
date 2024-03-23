import os
import re
import sys
import json
import django
from django.db import models
from django.core.files.base import ContentFile

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from data.scraper import DUMP_PATH, IMAGE_PATH
from data.models_dto import (
    TagDTO,
    UnitDTO,
    PromoDTO,
    ProductDTO,
    CategoryDTO,
    CharacteristicsDTO,
)
from utils import get_slug, image_filename
from mixins import BaseMixin, IconMixin
from products.models import Product, Measure, Unit, Characteristics
from promotion.models import PromoAction
from categories.models import Category
from tags.models import Tag, ProductTag


class JsonDumpReader(object):
    def read(
        self,
        path: str | Path,
    ) -> dict:
        with open(path, "r") as file:
            data = file.read()
        return data

    def read_all(
        self,
    ) -> tuple[list[PromoDTO], list[CategoryDTO]]:
        files_paths = os.listdir(DUMP_PATH)
        categories_paths = [p for p in files_paths if p.startswith("category")]
        promos_paths = [p for p in files_paths if p.startswith("promo")]

        promos: list[PromoDTO] = []
        for promo_path in promos_paths:
            promo = self.read(DUMP_PATH / promo_path)
            promo = PromoDTO.model_validate_json(promo)
            promos.append(promo)

        categories: list[CategoryDTO] = []
        for category_path in categories_paths:
            category = self.read(DUMP_PATH / category_path)
            category = CategoryDTO.model_validate_json(category)
            categories.append(category)

        return promos, categories


class JsonDataAdder(object):
    def upload_image(self, path: str) -> bytes:
        with open(IMAGE_PATH / path, "rb") as file:
            data = file.read()
        return data

    def add_icon(
        self,
        instance: IconMixin,
        image_path: str,
    ) -> None:
        if not instance.icon:
            img_bytes = self.upload_image(image_path)
            image_name = image_filename(instance, image_path)
            image_content = ContentFile(img_bytes, image_name)
            instance.icon.save(image_name, image_content)

    def add_image(
        self,
        instance: BaseMixin,
        image_path: str,
    ) -> None:
        if not instance.image:
            img_bytes = self.upload_image(image_path)
            image_name = image_filename(instance, image_path)
            image_content = ContentFile(img_bytes, image_name)
            instance.image.save(image_name, image_content)

    def add_category(
        self,
        categoryDTO: CategoryDTO,
    ) -> None:
        slug = get_slug(Category, categoryDTO.name)
        categoryORM = Category.objects.create(
            name=categoryDTO.name,
            slug=slug,
        )

        self.add_image(categoryORM, categoryDTO.image_path)
        self.add_icon(categoryORM, categoryDTO.image_path)
        categoryDTO.id = categoryORM.id

    def add_measure(
        self,
        characteristics: CharacteristicsDTO,
    ) -> None:
        Measure.objects.get_or_create(
            name=characteristics.measure,
            symbol=characteristics.measure_symbol,
        )

    def add_measures(
        self,
        categoriesDTOS: list[CategoryDTO],
    ) -> None:
        for categoryDTO in categoriesDTOS:
            for productDTO in categoryDTO.products:
                for unitDTO in productDTO.units:
                    charchs = unitDTO.characteristics
                    self.add_measure(charchs)

    def add_characteristics(
        self,
        unitDTO: UnitDTO,
        unitORM: Unit,
    ) -> None:
        charchs = unitDTO.characteristics
        measureORM = Measure.objects.get(
            name=charchs.measure,
            symbol=charchs.measure_symbol,
        )

        Characteristics.objects.create(
            measure_count=charchs.measure_count,
            quantity=charchs.quantity,
            proteins=charchs.proteins,
            fats=charchs.fats,
            carbohydrates=charchs.carbohydrates,
            kilocalories=charchs.kilocalories,
            unit=unitORM,
            measure=measureORM,
        )

    def add_tag(self, tagDTO: TagDTO) -> None:
        tagORM, _ = Tag.objects.get_or_create(
            name=tagDTO.name,
        )
        self.add_image(tagORM, tagDTO.image_path)

    def add_tags(
        self,
        categoriesDTOS: list[CategoryDTO],
    ) -> None:
        for categoryDTO in categoriesDTOS:
            for productDTO in categoryDTO.products:
                for tagDTO in productDTO.tags:
                    self.add_tag(tagDTO)

    def add_units(
        self,
        productDTO: ProductDTO,
        productORM: Product,
    ) -> None:
        for unitDTO in productDTO.units:
            unitORM = Unit.objects.create(
                product=productORM,
                name=unitDTO.name,
                price=unitDTO.price,
                discount_price=unitDTO.discount_price,
            )
            unitDTO.id = unitORM.id

            self.add_characteristics(unitDTO, unitORM)

    def add_product_tags(
        self,
        productDTO: ProductDTO,
        productORM: Product,
    ) -> None:
        for tagDTO in productDTO.tags:
            tagORM = Tag.objects.get(name=tagDTO.name)
            ProductTag.objects.create(
                tag=tagORM,
                product=productORM,
            )

    def add_products(
        self,
        categoryDTO: CategoryDTO,
    ) -> None:
        for productDTO in categoryDTO.products:
            categoryORM = Category.objects.get(id=categoryDTO.id)
            slug = get_slug(Product, productDTO.name)

            productORM = Product(
                name=productDTO.name,
                description=productDTO.description,
                slug=slug,
                category=categoryORM,
            )
            productDTO.id = productORM.id
            self.add_image(productORM, productDTO.image_path)

            self.add_units(productDTO, productORM)
            self.add_product_tags(productDTO, productORM)

    def add_products_data(
        self,
        categoriesDTOS: list[CategoryDTO],
    ) -> None:
        for categoryDTO in categoriesDTOS:
            self.add_category(categoryDTO)

        self.add_measures(categoriesDTOS)
        self.add_tags(categoriesDTOS)

        for categoryDTO in categoriesDTOS:
            self.add_products(categoryDTO)

    def add_promos(
        self,
        promosDTOS: list[ProductDTO],
    ) -> None:
        for promoDTO in promosDTOS:
            slug = get_slug(PromoAction, promoDTO.name)

            promoORM = PromoAction.objects.create(
                name=promoDTO.name,
                description=promoDTO.description,
                slug=slug,
            )
            self.add_image(promoORM, promoDTO.image_path)


if __name__ == "__main__":
    reader = JsonDumpReader()
    adder = JsonDataAdder()

    promos, categories = reader.read_all()

    adder.add_promos(promos)
    adder.add_products_data(categories)
