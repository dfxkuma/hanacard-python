import aiohttp
import asyncio
import ssl
import json
import urllib.parse


async def main():
    ssl_context = ssl.create_default_context()
    ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')
    ios6_agent = ("Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) "
                  "AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 "
                  "Mobile/10A5376e Safari/8536.25")

    cookie_jar = aiohttp.CookieJar(unsafe=True)
    session = aiohttp.ClientSession(
        cookie_jar=cookie_jar,
        connector=aiohttp.TCPConnector(ssl=ssl_context),
        headers={'User-Agent': ios6_agent},
    )

    async with session.post('https://m.hanacard.co.kr/MKLGN2110M.ajax') as response:
        response_json = json.loads(await response.text())
        print(response_json)
        pay_login_code = response_json['DATA']['EASN_LGN_CTF_ID']  # 하나페이 로그인 앱 열때 필요한 코드

        print("인증코드: ", pay_login_code)
        _app_scheme = f"oneqpay://app_card_auth" + urllib.parse.urlencode({
            'intro': 'on',
            'ch': 'W',  # 웹 채널
            'tc': '01',
            'tid': pay_login_code,
        })

asyncio.run(main())
