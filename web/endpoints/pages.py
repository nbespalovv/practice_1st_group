from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse


router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_auth_page(request: Request, tg_uid=Cookie(None)):
    if tg_uid is not None:
        return RedirectResponse("/user")
    return templates.TemplateResponse("root.html", {"request": request})


@router.get("/user")
def get_user_page(request: Request):
    """Страница авторизованного пользователя"""
    return templates.TemplateResponse("user.html", {"request": request})