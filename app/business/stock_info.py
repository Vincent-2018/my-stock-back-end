from app.datatype.stock_info import (
    StockInfo,
    GetStockInfoMdl,
    GetStockInfoListMdl,
    CreateStockInfoMdl,
    UpdateStockInfoMdl
)
from app.initializer import g
from app.utils import auth, db_async
from fastapi.encoders import jsonable_encoder


class GetStockInfoBiz(GetStockInfoMdl):

    async def get(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=StockInfo,
                fields=self.response_fields(),
                filter_by={"id": self.id},
            )
            if data:
                # 直接使用 jsonable_encoder 处理包含 datetime 的数据
                encoded_data = jsonable_encoder(data)
                return encoded_data
            return None


class GetStockInfoListBiz(GetStockInfoListMdl):

    async def get_list(self):
        async with g.db_async_session() as session:
            data = await db_async.query_all(
                session=session,
                model=StockInfo,
                fields=self.response_fields(),
                page=self.page,
                size=self.size,
            )
            total = await db_async.query_total(session, StockInfo)
            if data:
                # 使用 jsonable_encoder 处理每个数据项
                items = [jsonable_encoder(item) for item in data]
                return items, total
            return [], 0

    async def post_list(self):
        async with g.db_async_session() as session:
            # 构建过滤条件
            filter_by = {}
            for field in self.response_fields():
                value = getattr(self, field)
                if value is not None:
                    filter_by[field] = value

            # 查询数据
            data = await db_async.query_all(
                session=session,
                model=StockInfo,
                fields=self.response_fields(),
                filter_by=filter_by,
                page=self.page,
                size=self.size,
            )
            total = await db_async.query_total(
                session=session,
                model=StockInfo,
                filter_by=filter_by
            )

            if data:
                # 处理datetime等特殊类型
                items = [jsonable_encoder(item) for item in data]
                return items, total
            return [], 0


class CreateStockInfoBiz(CreateStockInfoMdl):

    async def create(self):
        async with g.db_async_session() as session:
            return await db_async.create(
                session=session,
                model=StockInfo,
                data={
                    "type": self.type,
                    "grant_date": self.grant_date,
                    "available_sell_quantity": self.available_sell_quantity,
                    "stock_option_anchors_price": self.stock_option_anchors_price,
                    "stock_price": self.stock_price,
                    "value_usd": self.value_usd,
                    "value_cny": self.value_cny,
                }
            )


class UpdateStockInfoBiz(UpdateStockInfoMdl):

    async def update(self, stock_info_id: str):
        async with g.db_async_session() as session:
            return await db_async.update(
                session=session,
                model=StockInfo,
                data=self.model_dump(),
                filter_by={"id": stock_info_id},
            )


class DeleteStockInfoBiz:

    @staticmethod
    async def delete(stock_info_id: str):
        async with g.db_async_session() as session:
            return await db_async.delete(
                session=session,
                model=StockInfo,
                filter_by={"id": stock_info_id},
            )