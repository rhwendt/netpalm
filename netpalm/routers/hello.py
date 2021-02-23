import logging

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from netpalm.backend.core.models.models import Hello
from netpalm.backend.core.models.ncclient import NcclientHello
from netpalm.backend.core.models.task import Response
from netpalm.routers.route_utils import error_handle_w_cache, whitelist
from netpalm.backend.core.redis import reds

log = logging.getLogger(__name__)
router = APIRouter()


def _hello(hello: Hello, library: str = None):
    req_data = hello.dict(exclude_none=True)
    if library is not None:
        req_data["library"] = library
    r = reds.execute_task(method="hello", kwargs=req_data)
    resp = jsonable_encoder(r)
    return resp


@router.post("/hello", response_model=Response, status_code=201)
@error_handle_w_cache
@whitelist
def hello(hello: Hello):
    return _hello(hello)


@router.post("/hello/ncclient", response_model=Response, status_code=201)
@error_handle_w_cache
@whitelist
def hello_ncclient(hello: NcclientHello):
    return _hello(hello, library='ncclient')
