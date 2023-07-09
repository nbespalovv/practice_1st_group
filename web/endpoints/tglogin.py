import hmac
from hashlib import sha256
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Query
from fastapi import Depends
from fastapi.responses import RedirectResponse
import json

from deps import get_db
from pydantic import Field

from schemas.link import Link, LinkInDB, LinkUpdate
import crud.links as crud
from core.broker import session #заменить с ребита

router = APIRouter(prefix="/tglogin")

BOT_TOKEN = '6001783957:AAGjtyLX2728zncYkhCDMIq0_MsasMBtOY0'

#Авторизация по тг#
@router.get('/')
def get_link(id: int, first_name: str, auth_date: int, hash: str,  last_name: Optional[str] = Query(None),  username: Optional[str] = Query(None), photo_url: Optional[str] = Query(None), db=Depends(get_db)):
    fields = dict({"id": id, "first_name": first_name, 'username': username, 'photo_url': photo_url, 'auth_date': auth_date, 'hash': hash, 'last_name': last_name})
    hash = fields.pop('hash')
    auth_date = fields.get('auth_date')
    id = fields.get('id')
    fields = dict(sorted(fields.items(), key=lambda item: item[0]))
    data_check_string = ('\n'.join('='.join((key, str(val))) for (key, val) in fields.items()))
    secret = sha256(BOT_TOKEN.encode('utf-8'))
    sig = hmac.new(secret.digest(), data_check_string.encode('utf-8'), sha256).hexdigest()
    if sig == hash:
        response = RedirectResponse('/')
        response.set_cookie(key="token", value=hash)
        response.set_cookie(key="tg_uid", value=id)
        response.set_cookie(key="tg_uname", value=username)
        return response
    return "Error while logging in"