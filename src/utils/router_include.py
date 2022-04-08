from os import listdir
from os.path import join, isdir, isfile
from importlib import import_module
from fastapi import APIRouter


def _include_router():
    '''
    動的にAPI Routerを追加していく
    '''
    _router = APIRouter()
    src_dir = "src"
    module_dir = "routers"
    router_file = "router.py"
    path = join(src_dir, module_dir)

    print(path)
    for api_dir in [dir for dir in listdir(path) if isdir(join(path, dir))]:
        api_file = join(path, api_dir, router_file)
        print(api_file)

        if isfile(api_file):
            module = import_module(f"{src_dir}.{module_dir}.{api_dir}.router")
            module_router = module.router
            module_prefix = module.prefix
            module_tags = module.tags

            print(module_router)
            print(module_prefix)
            print(module_tags)

            _router.include_router(router=module_router,
                                   prefix=module_prefix, tags=module_tags)

            print(f"Module Add Item : {api_dir}")

    return _router


router = _include_router()
