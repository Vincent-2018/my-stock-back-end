import traceback

from fastapi import APIRouter, Depends

from app.api.response import Response, response_docs
from app.business.stock_info import (
    GetStockInfoBiz,
    GetStockInfoListBiz,
    CreateStockInfoBiz,
    UpdateStockInfoBiz,
    DeleteStockInfoBiz
)
from app.api.status import Status
from app.initializer import g
from app.middleware.auth import JWTUser, get_current_user
from app.utils.format_utils import format_timestamps

stock_info_router = APIRouter()
_active = True  # 激活(若省略则默认True)


@stock_info_router.get(
    path="/stock_info/{stock_info_id}",
    summary="股票信息详情",
    responses=response_docs(
        model=GetStockInfoBiz,
    ),
)
async def get(
        stock_info_id: str,
        current_user: JWTUser = Depends(get_current_user),  # 认证
):
    try:
        stock_info_biz = GetStockInfoBiz(id=stock_info_id)
        data = await stock_info_biz.get()
        data = format_timestamps(data)
        if not data:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="stock_info详情失败", error=e)
    return Response.success(data=data)


@stock_info_router.get(
    path="/stock_info",
    summary="股票信息列表",
    responses=response_docs(
        model=GetStockInfoListBiz,
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
        stock_info_biz = GetStockInfoListBiz(page=page, size=size)
        data, total = await stock_info_biz.get_list()
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="获取股票信息列表失败", error=e)
    return Response.success(data={"items": data, "total": total})


@stock_info_router.post(
    path="/stock_info",
    summary="创建股票信息",
    responses=response_docs(model=CreateStockInfoBiz),
)
async def create(
    stock_info: CreateStockInfoBiz,
    current_user: JWTUser = Depends(get_current_user),
):
    try:
        data = await stock_info.create()
        if not data:
            return Response.failure(msg="创建股票信息失败")
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="创建股票信息失败", error=e)
    return Response.success(data=data)


@stock_info_router.put(
    path="/stock_info/{stock_info_id}",
    summary="更新股票信息",
    responses=response_docs(model=UpdateStockInfoBiz),
)
async def update(
    stock_info_id: str,
    stock_info: UpdateStockInfoBiz,
    current_user: JWTUser = Depends(get_current_user),
):
    try:
        updated_ids = await stock_info.update(stock_info_id)
        if not updated_ids:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="更新股票信息失败", error=e)
    return Response.success(data={"stock_info_id": stock_info_id})


@stock_info_router.delete(
    path="/stock_info/{stock_info_id}",
    summary="删除股票信息",
    responses=response_docs(),
)
async def delete(
    stock_info_id: str,
    current_user: JWTUser = Depends(get_current_user),
):
    try:
        deleted_count = await DeleteStockInfoBiz.delete(stock_info_id)
        if not deleted_count:
            return Response.failure(msg="未匹配到记录", status=Status.RECORD_NOT_EXIST_ERROR)
    except Exception as e:
        g.logger.error(traceback.format_exc())
        return Response.failure(msg="删除股票信息失败", error=e)
    return Response.success(data={"stock_info_id": stock_info_id})