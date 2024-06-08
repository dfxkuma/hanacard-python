from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ssl
from aiohttp import ClientSession, TCPConnector, FormData, CookieJar
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# SSL 설정 및 User-Agent 설정
ssl_context = ssl.create_default_context()
ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')
ios6_agent = "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"

# CookieJar와 ClientSession 초기화
cookie_jar = CookieJar()
session: ClientSession = None


async def create_session() -> ClientSession:
    global session
    if session is None:
        session = ClientSession(cookie_jar=cookie_jar, connector=TCPConnector(ssl=ssl_context), headers={
            'User-Agent': ios6_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
        })
    return session


@app.on_event("startup")
async def startup_event():
    global session
    session = await create_session()


@app.on_event("shutdown")
async def shutdown_event():
    await session.close()


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.get("/get_recent")
async def get_recent():
    session = await create_session()
    form_data = FormData()
    form_data.add_field('targetMethod', 'getRecentUsedHistory')
    async with session.post('https://m.hanacard.co.kr/MKMAIN1010M.ajax', data=form_data) as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json


@app.get("/auth_verify")
async def auth_verify():
    session = await create_session()
    async with session.post('https://m.hanacard.co.kr/MKLGN2120M.ajax') as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json


@app.get("/login/app")
async def login_app():
    # 하나카드 앱 로그인
    session = await create_session()
    form_data = FormData()
    form_data.add_field('_nFilterEncryptValue', '')
    async with session.post(
            'https://m.hanacard.co.kr/MKLGN2130M.ajax',
            data=form_data
    ) as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json


@app.get("/login/pass")
async def login_pass():
    # PASS 앱 로그인
    session = await create_session()
    async with session.post(
        'https://m.hanacard.co.kr/MKLGN2210M.ajax',
    ) as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json


@app.get("/code/pass")
async def login_code_pass():
    # PASS 앱 요청 보내기
    session = await create_session()
    form_data = FormData()
    form_data.add_field('targetMethod', 'passAuthReq')
    form_data.add_field('menuUri', 'MKLGN2200M.web')
    form_data.add_field('APLP_NM', '홍길동')  # 이름
    form_data.add_field('BIRD', '11110101')  # 생년월일 8자리
    form_data.add_field('SSN', '')
    form_data.add_field('MMT_TCC_CO_DC', '2')  # 통신사 1: SKT, 2: KT, 3: LGU+, 4: SKT 알뜰폰, 5: KT 알뜰폰, 6: LGU+ 알뜰폰
    form_data.add_field('CELL_NO', '01012345678')  # 휴대폰 번호
    async with session.post(
            'https://m.hanacard.co.kr/ITAUTH9210M.ajax',
            data=form_data
    ) as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json


@app.get("/code/pass/verify")
async def login_code_pass_verify():
    # PASS 앱 인증 확인
    session = await create_session()
    form_data = FormData()
    form_data.add_field('targetMethod', 'passAuthReq')
    form_data.add_field('menuUri', 'MKLGN2200M.web')
    async with session.post(
            'https://m.hanacard.co.kr/ITAUTH9220M.ajax',
            data=form_data
    ) as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json


@app.get("/code/app")
async def login_code_app():
    # 하나카드 앱 로그인 코드 생성
    session = await create_session()
    async with session.post(
        'https://m.hanacard.co.kr/MKLGN2110M.ajax',
        headers={'Content-Type': 'application/json'},
        data={}
    ) as response:
        response_text = await response.text()
        response_json = json.loads(response_text)
        return response_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
