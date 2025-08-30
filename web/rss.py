from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Response

router = APIRouter(
    prefix="/rss", tags=["RSS Feed"], responses={404: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")


@router.get("/feed.xml", response_class=Response)
async def rss_feed(request: Request):
    xml_content = templates.get_template("rss.xml").render(request=request, posts=posts)
    return Response(content=xml_content, media_type="application/rss+xml")
