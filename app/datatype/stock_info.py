from pydantic import BaseModel, Field
from decimal import Decimal
from sqlalchemy import Column, String, DECIMAL, BigInteger, DateTime
from toollib.utils import now2timestamp
from app.datatype import DeclBase, filter_fields
from app.initializer import g
from datetime import datetime



class StockInfo(DeclBase):
    __tablename__ = "biz_stock_info"

    id = Column(String(100), primary_key=True, default=g.snow.gen_uid, comment="股票信息id")
    type = Column(String(20), nullable=False, comment="股票类型")
    grant_date = Column(DateTime, nullable=False, comment="授予日期")
    available_sell_quantity = Column(BigInteger, nullable=False, comment="可售数量")
    stock_option_anchors_price = Column(DECIMAL(10, 2), nullable=False, comment="股票期权锚定价格")
    stock_price = Column(DECIMAL(10, 2), nullable=False, comment="股票价格")
    value_usd = Column(DECIMAL(10, 2), nullable=False, comment="价值美元")
    value_cny = Column(DECIMAL(10, 2), nullable=False, comment="价值人民币")
    created_at = Column(BigInteger, default=now2timestamp, comment="创建时间")
    updated_at = Column(BigInteger, default=now2timestamp, onupdate=g.now2timestamp, comment="更新时间")


class GetStockInfoMdl(BaseModel):
    id: str = Field(...)
    type: str = None
    grant_date: datetime = None
    available_sell_quantity: int = None
    stock_option_anchors_price: float = None
    stock_price: float = None
    value_usd: float = None
    value_cny: float = None

    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[]
        )


class GetStockInfoListMdl(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1)
    id: str = None
    type: str = None
    grant_date: datetime = None
    available_sell_quantity: int = None
    stock_option_anchors_price: float = None
    stock_price: float = None
    value_usd: float = None
    value_cny: float = None
    created_at: int = None
    updated_at: int = None
    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[
                "page",
                "size",
            ]
        )


class CreateStockInfoMdl(BaseModel):
    type: str | None = Field(None)
    grant_date: datetime | None = Field(None)
    available_sell_quantity: int | None = Field(None)
    stock_option_anchors_price: Decimal | None = Field(None)
    stock_price: Decimal | None = Field(None)
    value_usd: Decimal | None = Field(None)
    value_cny: Decimal | None = Field(None)


class UpdateStockInfoMdl(BaseModel):
    type: str | None = Field(None)
    grant_date: datetime | None = Field(None)
    available_sell_quantity: int | None = Field(None)
    stock_option_anchors_price: Decimal | None = Field(None)
    stock_price: Decimal | None = Field(None)
    value_usd: Decimal | None = Field(None)
    value_cny: Decimal | None = Field(None)

class DeleteStockInfoMdl(BaseModel):
    pass
