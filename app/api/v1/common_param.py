import traceback

from fastapi import APIRouter, Depends

from app.api.response import Response, response_docs
from app.business.common_param import (
    GetCommonParamBiz,
)
from app.api.status import Status
from app.initializer import g
from app.middleware.auth import JWTUser, get_current_user

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
        common_param_id: str,
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
