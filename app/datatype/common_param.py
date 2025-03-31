from pydantic import BaseModel, Field
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