from pydantic import BaseModel


class ImageMixin(BaseModel):
    image_url: str
    image_path: str


class NameMixin(BaseModel):
    name: str


class TagDTO(
    NameMixin,
    ImageMixin,
    BaseModel,
):
    pass


class CharacteristicsDTO(BaseModel):
    measure: str
    measure_symbol: str
    measure_count: int
    quantity: int

    proteins: int | None
    fats: int | None
    carbohydrates: int | None
    kilocalories: int | None


class UnitDTO(BaseModel):
    name: str | None
    price: int
    discount_price: int | None
    characteristics: CharacteristicsDTO


class ProductDTO(
    NameMixin,
    ImageMixin,
    BaseModel,
):
    description: str
    tags: list[TagDTO]
    units: list[UnitDTO]


class CategoryDTO(
    NameMixin,
    ImageMixin,
    BaseModel,
):
    products: list[ProductDTO]


class PromoDTO(
    NameMixin,
    ImageMixin,
    BaseModel,
):
    description: str
