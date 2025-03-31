import re
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, field_serializer
from sqlalchemy import Column, String, DECIMAL, BigInteger
from app.datatype import DeclBase, filter_fields
from app.initializer import g


class CommonParam(DeclBase):
    __tablename__ = "biz_common_param"

    id = Column(BigInteger, primary_key=True, default=g.snow.gen_uid, comment="主键")
    name = Column(String(100), nullable=False, comment="参数名称")
    value = Column(DECIMAL(10, 2), nullable=False, comment="参数值")


class GetCommonParamMdl(BaseModel):
    id: int = Field(...)
    name: str = None
    value: float = None

    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[]
        )

class GetCommonParamListMdl(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1)
    id: int = None
    name: str = None
    value: float = None

    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[
                "page",
                "size",
            ]
        )
    
class CreateCommonParamMdl(BaseModel):
    name: str | None = Field(None)
    value: Decimal | None = Field(None)

    @field_validator("name")
    def validate_name(cls, v, info):
        if not v and (name := info.data.get("name")):
            return f"参数名称{name[-4:]}"
        if v and not re.match(r"^[\u4e00-\u9fffA-Za-z0-9_\-.]{1,50}$", v):
            raise ValueError("参数名称仅限1-50位的中文、英文、数字、_-.组合")
        return v

    @field_validator("value", mode="before")
    def validate_value(cls, v):
        if isinstance(v, str):
            return Decimal(v)  # 将字符串转换为 Decimal
        return v

    @field_serializer("value")
    def format_value(cls, v: Decimal) -> str:
        return f"{v:.2f}"  # 保留两位小数并返回字符串