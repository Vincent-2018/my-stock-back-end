from app.datatype.common_param import (
    CommonParam,
    GetCommonParamMdl,
    GetCommonParamListMdl,
)
from app.initializer import g
from app.utils import auth, db_async

class GetCommonParamBiz(GetCommonParamMdl):

    async def get(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=CommonParam,
                fields=self.response_fields(),
                filter_by={"id": self.id},
            )
            if data:
                # 使用 Pydantic 模型进行验证和转换
                return GetCommonParamMdl(**data).model_dump()
            return None
        
class GetCommonParamListBiz(GetCommonParamListMdl):

    async def get_list(self):
        async with g.db_async_session() as session:
            data = await db_async.query_all(
                session=session,
                model=CommonParam,
                fields=self.response_fields(),
                page=self.page,
                size=self.size,
            )
            total = await db_async.query_total(session, CommonParam)
            if data:
                # 对每一条记录进行 Pydantic 模型验证和转换
                items = [GetCommonParamMdl(**item).model_dump() for item in data]
                return items, total
            return [], 0