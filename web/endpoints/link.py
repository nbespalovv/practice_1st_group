from fastapi import APIRouter, HTTPException, status, Cookie
from fastapi import Depends
import json

# from deps import get_db

from web.workers.parser_worker import parse_website

router = APIRouter(prefix="/parse")


@router.get("/")
async def parse_endpoint(name: str):
    try:
        task = parse_website.delay(name)  # не ебу че туда закинуть пока что
        return task.id
    except HTTPException as e:
        raise e

#
# @router.post('/', response_model=LinkInDB)
# def post_link(link: Link, tg_uid: int = Cookie(None), db=Depends(get_db)):
#     """Метод для создания ссылки в базе данных"""
#     result = crud.create_link(db=db, url=link.url)
#     dict_values = result.as_dict()
#     dict_values['tg_uid'] = tg_uid
#     session.publish_task(json.dumps(dict_values))
#     return LinkInDB(id=result.id, url=result.url, result_url=result.result_url)
#
#
# @router.get('/', response_model=LinkInDB)
# def get_link(id: int, db=Depends(get_db)):
#     """Метод для получения ссылки из базы данных"""
#     result = crud.get_link_by_id(db=db, id=id)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return LinkInDB(id=result.id, url=result.url, result_url=result.result_url)
#
#
# @router.put('/', response_model=LinkInDB)
# def update_link(link: LinkUpdate, db=Depends(get_db)):
#     """Метод для обвновления состояния ссылки"""
#     result = crud.update_result_url_by_id(db=db, id=link.id, result_url=link.result_url)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return LinkInDB(id=result.id, url=result.url, result_url=result.result_url)
