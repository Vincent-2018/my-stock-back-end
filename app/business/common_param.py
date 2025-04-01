from app.datatype.common_param import (
    CommonParam,
    GetCommonParamMdl,
    GetCommonParamListMdl,
    CreateCommonParamMdl,
    UpdateCommonParamMdl,
    DeleteCommonParamMdl,
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
        
class CreateCommonParamMdlBiz(CreateCommonParamMdl):

    async def create(self):
        async with g.db_async_session() as session:
            return await db_async.create(
                session=session,
                model=CommonParam,
                data={
                    "name": self.name,
                    "value": self.value,
                },
                filter_by={"name": self.name},
            )

class UpdateCommonParamBiz(UpdateCommonParamMdl):

    async def update(self, common_param_id: str):
        async with g.db_async_session() as session:
            return await db_async.update(
                session=session,
                model=CommonParam,
                data=self.model_dump(),
                filter_by={"id": common_param_id},
            )

class DeleteCommonParamBiz(DeleteCommonParamMdl):

    @staticmethod
    async def delete(common_param_id: str):
        async with g.db_async_session() as session:
            return await db_async.delete(
                session=session,
                model=CommonParam,
                filter_by={"id": common_param_id},
            )