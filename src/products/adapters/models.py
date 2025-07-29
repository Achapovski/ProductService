import uuid
from decimal import Decimal

from sqlalchemy import VARCHAR, UUID, DECIMAL, ForeignKey, BOOLEAN, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.metadata import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(45), nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(6, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(DECIMAL(3, 1), default=Decimal("0.0"))
    is_active: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    image_title_prefix: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    # TODO: "Create Date" field ?

    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("types.id"))
    collection_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collections.id"))

    type: Mapped["Type"] = relationship(back_populates="products")
    colors: Mapped[list["Color"]] = relationship(back_populates="products", secondary="product_colors")
    materials: Mapped[list["Material"]] = relationship(back_populates="products", secondary="product_materials")
    images: Mapped[list["Image"]] = relationship(back_populates="product")
    categories: Mapped[list["Category"]] = relationship(back_populates="products", secondary="product_categories")
    collection: Mapped["Collection"] = relationship(back_populates="products")


class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(45), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    discount: Mapped[Decimal] = mapped_column(DECIMAL(3, 1), default=Decimal("0.0"))
    is_active: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="collection")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(45), nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="categories", secondary="product_categories")


class Color(Base):
    __tablename__ = "colors"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(25), nullable=False, unique=True)

    products: Mapped[list[Product]] = relationship(back_populates="colors", secondary="product_colors")


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(45), nullable=False, unique=True)

    products: Mapped[list[Product]] = relationship(back_populates="materials", secondary="product_materials")


class Type(Base):
    __tablename__ = "types"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(35), nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="type")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, unique=True)
    main: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=True)

    product_image_title_prefix: Mapped[str] = mapped_column(VARCHAR(100), ForeignKey("products.image_title_prefix"))
    product: Mapped["Product"] = relationship(back_populates="images")


class ProductMaterials(Base):
    __tablename__ = "product_materials"

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
    material_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("materials.id"), primary_key=True)


class ProductColors(Base):
    __tablename__ = "product_colors"

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
    color_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("colors.id"), primary_key=True)


class ProductCategories(Base):
    __tablename__ = "product_categories"

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"), primary_key=True)
