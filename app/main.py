from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .containers import Container
from .helpers.trie import Trie
from .services import DictionaryService


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MIN_PREFIX_LENGTH = 3
suggestion_trie = Trie()


@app.on_event("startup")
@inject
async def startup_event(dictionary_service: DictionaryService = Depends(Provide[Container.service])):
    # await dictionary_service.clear()
    dictionary = dictionary_service.load_dictionary()
    dictionary_service.populate_trie(suggestion_trie, dictionary.keys())
    # await dictionary_service.populate(dictionary)


@app.api_route("/")
async def index(request: Request):
    return templates.TemplateResponse('search.html', {"request": request})


@app.api_route("/search")
async def search(request: Request):
    prefix = request.query_params.get("search")
    suggestions = suggestion_trie.search(prefix)[:5]
    return templates.TemplateResponse('suggestions.html', {"request": request, "words": suggestions})


@app.api_route("/translate")
@inject
async def search(request: Request, service: DictionaryService = Depends(Provide[Container.service])):
    value = await service.get_article(request.query_params.get("search").lower())
    return templates.TemplateResponse('results.html', {"request": request, "value": value})


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.config.redis_password.from_env("REDIS_PASSWORD", "password")
container.wire(modules=[__name__])
