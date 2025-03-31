import traceback

from fastapi import APIRouter, Depends
from app.api.response import Response, response_docs
from app.business.common_param import (
    GetCommonParamBiz,
    GetCommonParamListBiz,
    CreateCommonParamMdlBiz
)
from app.api.status import Status
from app.initializer import g
from app.middleware.auth import JWTUser, get_current_user
from loguru import logger

common_param_router = APIRouter()
_active = True  # 激活(若省略则默认True)


@common_param_router.get(
    path="/common_param/{common_param_id}",
    summary="common_param详情",
    responses=response_docs(
        model=GetCommonParamBiz,
    ),
)
async def get(
        common_param_id: int,
        current_user: JWTUser = Depends(get_current_user),  # 认证
):
    try:
        common_param_biz = GetCommonParamBiz(id=common_param_id)
        data = await common_param_biz.get()
        if not data:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="common_param详情失败", error=e)
    return Response.success(data=data)

@common_param_router.get(
    path="/common_param",
    summary="common_param列表",
    responses=response_docs(
        model=GetCommonParamListBiz,
        is_listwrap=True,
        listwrap_key="items",
        listwrap_key_extra={
            "total": "int",
        },
    ),
)
async def get_list(
        page: int = 1,
        size: int = 10,
        current_user: JWTUser = Depends(get_current_user),
):
    try:
        common_param_biz = GetCommonParamListBiz(page=page, size=size)
        data, total = await common_param_biz.get_list()
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="common_param列表失败", error=e)
    return Response.success(data={"items": data, "total": total})

# ------------------------------------
@common_param_router.post(
    path="/common_param",
    summary="common_param创建",
    responses=response_docs(data={
        "id": "int",
    }),
)
async def create(
        common_param_biz: CreateCommonParamMdlBiz,
):
    try:
        common_param_id = await common_param_biz.create()
        if not common_param_id:
            return Response.failure(msg="通用参数已存在", status=Status.RECORD_EXISTS_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="common_param创建失败", error=e)
    return Response.success(data={"id": common_param_id})
