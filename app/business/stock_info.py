from app.datatype.stock_info import (
    StockInfo,
    GetStockInfoMdl,
    GetStockInfoListMdl,
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