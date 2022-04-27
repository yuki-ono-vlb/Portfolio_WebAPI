from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.utils.router_include import router
from src.utils.database import create_db_and_tables
app = FastAPI()

@app.on_event("startup")
def on_seartup():
    create_db_and_tables()

@app.get("/", status_code=status.HTTP_403_FORBIDDEN)
async def index():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="閲覧権限がありません。")


def _create_origins():
    '''
    CORS origins
    '''
    protocols = [
        "http://",
        "https://"
    ]

    sub_domains = [
        "api",
        "www"
    ]

    domains = [
        "sgwp.xyz",
        "localhost",
        "app.test",
        "buildmake.xyz",
        "sk4869.info"
    ]

    ports = [
        80,
        443,
        3000,
        5000,
        8000,
        8080,
        443443,
    ]
    origins = []

    for domain,protocol,sub_domain,port in zip(domains,protocols,sub_domains,ports):
        for protocol in protocols:
            origins.append(f"{protocol}{domain}")
            for sub_domain in sub_domains:
                origins.append(f"{protocol}{sub_domain}.{domain}")
                for port in ports:
                    origins.append(f"{protocol}{domain}:{port}")
                    origins.append(f"{protocol}{sub_domain}.{domain}:{port}")

    return origins


app.include_router(router=router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=_create_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
