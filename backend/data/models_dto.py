from pydantic import BaseModel


class ImageMixin(BaseModel):
    image_url: str
    image_path: str


class NameMixin(BaseModel):
    name: str


class IDMixin(BaseModel):
    id: int | str | None


class TagDTO(
    IDMixin,
    NameMixin,
    ImageMixin,
    BaseModel,
):
    pass


class CharacteristicsDTO(
    IDMixin,
    BaseModel,
):
    measure: str
    measure_symbol: str
    measure_count: int
    quantity: int

    proteins: int | None
    fats: int | None
    carbohydrates: int | None
    kilocalories: int | None


class UnitDTO(
    IDMixin,
    BaseModel,
):
    name: str | None
    price: int
    discount_price: int | None
    characteristics: CharacteristicsDTO


class ProductDTO(
    IDMixin,
    NameMixin,
    ImageMixin,
    BaseModel,
):
    description: str
    tags: list[TagDTO]
    units: list[UnitDTO]


class CategoryDTO(
    IDMixin,
    NameMixin,
    ImageMixin,
    BaseModel,
):
    products: list[ProductDTO]


class PromoDTO(
    IDMixin,
    NameMixin,
    ImageMixin,
    BaseModel,
):
    description: str
