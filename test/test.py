import re
import asyncio
import aiohttp
from aiohttp.resolver import AsyncResolver
import ssl
import pathlib
import os
import base64
import qrcode
import time
import socket
from typing import List, Tuple, Optional
from urllib.parse import parse_qs, unquote, urlparse

project_dir = pathlib.Path(__file__).parent


# Create SSL context ONCE with session reuse
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE  # Skport cert validation for speed
DEFAULT_TIMEOUT = 6


async def CheckUrl(
    session: aiohttp.ClientSession, url: str
) -> Tuple[bool, Optional[float]]:
    try:
        start_time = time.time()

        async with session.get(
            url,
            ssl=SSL_CONTEXT,
            allow_redirects=True,
        ) as response:
            response_time = int((time.time() - start_time) * 1000)
            text = await response.text()
            print(response.status)
            if text:
                return True, response_time

            else:
                return False

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        pass

    return False


async def main():
    resolver = AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])

    connector = aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,  # Reuse SSL context
        force_close=True,  # Close connections after each request
        resolver=resolver,
    )
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)

    data = [
        "https://sync.watchwave.link/api/v1/rooms/63368e3dbb/sync",
        "https://639216722493642090.eslamshahr-sxft.beauty/ilmhlpws",
        "https://sync.watchwave.link/api/v1/rooms/63368e3dbb/sync",
        "https://titandarkness.mooo.com/21381/0ko2id8fmq",
        "https://titandarkness.mooo.com/21381/0ko2id8fmq",
        "https://www.calmlunch.com/assignment",
        "https://d1yxsk0zprgivr.cloudfront.net/",
        "https://ty986gfazs.cainiaohub.xyz/81574b6b-c9d7-44a0-b83d-dad56e8cb530",
    ]

    # async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    #     for link in data:
    #         text = await CheckUrl(session, link)
    #         print(text)

    d = (
        "vless://1a08570f-951b-409d-9e51-64c5df62e824@104.17.108.69:443?&security=tls&fp=chrome&sni=639216722493642090.eslamshahr-sxft.beauty&type=ws&headertype=none&host=639216722493642090.eslamshahr-sxft.beauty&path=%2filmhlpws#🇫🇷[openproxylist.com]",
        (False, 0),
    )
    print(d[1][0])


{
    "vless://4593aa27-a2a1-412f-935f-3829495c0970@91.235.234.186:443?encryption=none&flow=xtls-rprx-vision&type=tcp&security=reality&sni=us7fs3.proxen.pdevinfra.com&fp=qq&pbk=g-wqfhkjac71mmtkmq5bivtfavzxtcanei_17kotnsq#🇪🇪[openproxylist.com]": None,
    "vless://d9aa9ea3-9388-483f-a58d-a754f33ec505@gr048.bamajobin.ir:2053?mode=gun&security=reality&encryption=none&pbk=gs0dfvzx-bvkbdl2brvxsre6t2wyxxkfgp3x-mqc7by&fp=chrome&type=grpc&servicename=api.v1.data&sni=play.google.com&sid=524efc1f88592266#🇬🇧[openproxylist.com]": None,
    "vless://328af83b-29d8-4206-bc30-07e8afe03d2c@grsr1.plasdomain.ir:31993?security=reality&encryption=none&pbk=jji5mlufjwe8_effnind5hbnqpdhwweywgudegdtwwi&headertype=none&fp=qq&type=tcp&flow=xtls-rprx-vision&sni=play.google.com&sid=0e2f1c7219559d09#🇩🇪[openproxylist.com]": None,
    "vless://888193f6-6818-42f4-b223-64c9fd323b76@45.65.112.228:20513?encryption=none&type=tcp&security=reality&headertype=none&sni=updates.cdn-apple.com&fp=qq&pbk=ctfsure6fupyvbjgsmoynp3uketmmtjsqp45ocogi2k&sid=285db1978fd0d8c1#🇩🇪[openproxylist.com]": None,
    "vless://4fad9600-a7ec-47bd-b791-372c4b4fb792@104.168.90.119:443?security=reality&encryption=none&pbk=xrbare7hmasc6bz89-trcabtjsy5izwajoutu5swrqo&headertype=none&fp=chrome&spx=/89nmhrbc6rj5&type=tcp&flow=xtls-rprx-vision&sni=www.nvidia.com&sid=aad01fc116a8425c#🇺🇸[openproxylist.com]": None,
    "vless://41784775-8846-4579-9d9d-9ad6ea802e2e@185.141.227.141:40006?security=reality&sni=ads.x5.ru&fp=qq&pbk=uhciexxiceoz89kannbiksy4axpmsbb2xeomww7d1dy&sid=1a6b1f9d0e&type=tcp&flow=xtls-rprx-vision&packetencoding=xudp&encryption=none#🇪🇪[openproxylist.com]": None,
    "vless://44ae52b9-76fc-444d-8e43-186b4384b80a@free-amsterdam-node-1.cloudwidecdn.com:443?security=reality&encryption=none&pbk=prygoq51ilg0elupl9i0xcvmk1xpwkyfsr_tg4gnllu&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=www.apple.com&sid=1d86d17709852910#🇳🇱[openproxylist.com]": None,
    "vless://44ebd5d8-c8a3-408c-8195-1cb1e97c5c21@64.176.61.124:443?security=reality&encryption=none&pbk=kozjn-aqsors5axraykosu-xy-ndk3q8zh0xdwitfri&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=products.amd.com&sid=069fba81c72d1e#🇯🇵[openproxylist.com]": None,
    "vless://b1b3e430-ff52-44b8-b95d-27fa580fbc4f@ns.o11111o.club:443?encryption=none&fp=chrome&pbk=sbvkoemjk0silbwg4akybg5ml5kzwwb-ed4eee7ynrc&security=reality&servicename=vless-grpc-reality&sni=id.vk.com&type=grpc#🇩🇪[openproxylist.com]": None,
    "vless://22448df3-17f8-40a6-9199-babaca108b46@95.85.251.116:59631?mode=gun&security=reality&encryption=none&pbk=bymilcd_vndoof7qaq4qpftm-hmefpzwxptmfxdassg&fp=firefox&spx=%2fhesarweb&type=grpc&sni=google.com&sid=4b#🇫🇮[openproxylist.com]": None,
    "vless://c04bf2df-2b7f-44da-a893-3792d3910fd8@78.17.208.20:443?security=reality&type=tcp&packetencoding=xudp&sni=fr03.skorostnet.space&fp=chrome&flow=xtls-rprx-vision&sid=fdda9806fe5d8584&pbk=abnwkd8cvkuimbtzgsdnsiuieni-pqukkpuinlncz2o&encryption=none#🇫🇷[openproxylist.com]": None,
    "vless://f7c25743-140c-4d32-a296-a53bc49682d8@direct-nl.bachidze.com:443?flow=xtls-rprx-vision&headertype=none&fp=chrome&pbk=e12wxxagr8xuql7klwcltgmaxj74jcu__lg66yz6itw&security=reality&type=tcp&encryption=none&sni=direct-nl.bachidze.com#🇳🇱[openproxylist.com]": None,
    "trojan://uo36402987@54.216.124.178:443?security=tls&headertype=none&fp=chrome&type=tcp&sni=warm-bass.rooster465.autos#🇮🇪[openproxylist.com]": None,
    "vless://d9aa9ea3-9388-483f-a58d-a754f33ec505@54.37.6.119:2053?mode=gun&security=reality&encryption=none&pbk=gs0dfvzx-bvkbdl2brvxsre6t2wyxxkfgp3x-mqc7by&fp=firefox&type=grpc&servicename=api.v1.data&sni=play.google.com&sid=524efc1f88592266#🇬🇧[openproxylist.com]": None,
    "vless://7c9b4360-6be9-47f2-ace9-b87297ea3d8f@157.90.165.181:11762?security=reality&encryption=none&pbk=r2gkmf0tetlnesc1ppkzh9naoeehw-f5_u9jkg_clju&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=swdist.apple.com#🇩🇪[openproxylist.com]": None,
    "vless://1a08570f-951b-409d-9e51-64c5df62e824@104.17.108.69:443?&security=tls&fp=chrome&sni=639216722493642090.eslamshahr-sxft.beauty&type=ws&headertype=none&host=639216722493642090.eslamshahr-sxft.beauty&path=%2filmhlpws#🇫🇷[openproxylist.com]": None,
    "vless://166ef05e-8ab5-43b7-8910-d1bb0a4326a5@188.72.103.3:443?path=%2fapi%2fv1%2frooms%2f63368e3dbb%2fsync&security=tls&encryption=none&host=sync.watchwave.link&fp=chrome&type=ws&sni=cdn.tracker.yandex.net#🇳🇱[openproxylist.com]": None,
    "vless://7596b721-f311-4194-96e6-b7b407cd6083@89.23.103.121:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=qy222odlpfi9dvfohzngp0uhlubudtkllf_kmudy-ho&security=reality&sid=9795f83547c168d3&sni=www.debian.org&type=tcp#🇳🇱[openproxylist.com]": None,
    "vless://c124a209-d949-4951-8234-e2d918b3e6c0@188.225.33.206:8443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=c819rm4m_c473a8glp-ebfh8fm9o1cmeexmivdhm1fc&sni=max.ru#🇷🇺[openproxylist.com]": None,
    "vless://c04bf2df-2b7f-44da-a893-3792d3910fd8@185.232.117.114:443?encryption=none&flow=xtls-rprx-vision&fp=edge&pbk=abnwkd8cvkuimbtzgsdnsiuieni-pqukkpuinlncz2o&security=reality&sid=fdda9806fe5d8584&sni=vl04.skorostnet.space&type=tcp#🇬🇧[openproxylist.com]": None,
    "vless://c04bf2df-2b7f-44da-a893-3792d3910fd8@185.232.117.116:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=abnwkd8cvkuimbtzgsdnsiuieni-pqukkpuinlncz2o&sid=fdda9806fe5d8584&sni=vl06.skorostnet.space#🇬🇧[openproxylist.com]": None,
    "vless://d65cc14c-f53f-4fe2-b262-97856601319c@169.40.42.52:443?security=reality&encryption=none&pbk=e2rlf57li_-mdzge9ss1bwpgp54mqrb5pfxhw2jcvvg&headertype=&fp=ios&type=tcp&flow=xtls-rprx-vision&sni=yahoo.com&sid=c39cc7310a#🇺🇸[openproxylist.com]": None,
    "trojan://ba07a8af-5544-48ac-ab62-3b6c00a44fa6@oplosgru-c.catcat321.com:20004?security=tls&sni=hk.catxstar.com&type=tcp&path=/#🇯🇵[openproxylist.com]": None,
    "vless://b406bc51-9002-474c-beae-b194b02c91da@144.31.131.241:8443?flow=xtls-rprx-vision&security=reality&encryption=none&sni=mold.speedload.online&fp=chrome&pbk=j5itjbg5fqfembafkogkhhqb6digsfxqxk7xu-qmwus&sid=a20d3ed244c76426&type=tcp&path=%2f#🇲🇩[openproxylist.com]": None,
    "vless://f1c496bf-d2ab-45be-bc13-051d60d227b7@84.32.209.7:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=dartsearch-cn.net&fp=chrome&pbk=00n9lplaz0vgvrs57548s7xe0defc10pw2fkfhfpplm&type=tcp&headertype=none#🇱🇹[openproxylist.com]": None,
    "vless://564082ff-cf3c-48db-9e10-8ad2312847b4@81.19.137.181:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=tlpxtlz1y-v8b6q9mx55u6eypjfl0lcsne5zqp4yrhw&security=reality&sid=bbc68cec8bb8d2e3&sni=node21.mxvpn.dev&type=tcp#🇫🇷[openproxylist.com]": None,
    "vless://564082ff-cf3c-48db-9e10-8ad2312847b4@77.239.123.219:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=tlpxtlz1y-v8b6q9mx55u6eypjfl0lcsne5zqp4yrhw&security=reality&sid=bbc68cec8bb8d2e3&sni=node19.mxvpn.dev&type=tcp#🇩🇪[openproxylist.com]": None,
    "vless://564082ff-cf3c-48db-9e10-8ad2312847b4@144.31.65.68:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=tlpxtlz1y-v8b6q9mx55u6eypjfl0lcsne5zqp4yrhw&security=reality&sid=bbc68cec8bb8d2e3&sni=node18.mxvpn.dev&type=tcp#🇳🇱[openproxylist.com]": None,
    "vless://564082ff-cf3c-48db-9e10-8ad2312847b4@144.31.65.59:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=tlpxtlz1y-v8b6q9mx55u6eypjfl0lcsne5zqp4yrhw&security=reality&sid=bbc68cec8bb8d2e3&sni=node17.mxvpn.dev&type=tcp#🇳🇱[openproxylist.com]": None,
    "vless://4f375fb4-3c95-425f-bc7b-8085487a6f3c@titandarkness.mooo.com:443?encryption=none&fp=chrome&host=titandarkness.mooo.com&path=%2f21381%2f0ko2id8fmq&security=tls&sni=titandarkness.mooo.com&type=ws#🇧🇷[openproxylist.com]": None,
    "vless://4f375fb4-3c95-425f-bc7b-8085487a6f3c@177.3.208.169:443?&security=tls&fp=chrome&sni=titandarkness.mooo.com&type=ws&headertype=none&host=titandarkness.mooo.com&path=%2f21381%2f0ko2id8fmq#🇧🇷[openproxylist.com]": None,
    "vless://89755337-8050-401c-86d1-c8c34fb88d89@46.8.158.22:443?security=reality&encryption=none&pbk=wdwqnp1lnafz3l_r9hrk5vpvgv9m7ubb5jzuypcwdae&headertype=none&fp=chrome&spx=/&type=tcp&sni=www.icloud.com&sid=e96bc8c85c3836#🇷🇺[openproxylist.com]": None,
    "vless://d65cc14c-f53f-4fe2-b262-97856601319c@169.40.42.133:443?security=reality&encryption=none&pbk=e2rlf57li_-mdzge9ss1bwpgp54mqrb5pfxhw2jcvvg&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=yahoo.com&sid=c39cc7310a#🇺🇸[openproxylist.com]": None,
    "vless://cd5cf6e7-7ce5-42c9-9316-68210fa72a32@13.193.205.133:27407?security=reality&encryption=none&pbk=sajk6lzhbkkflexjiwseyqbpezgpiop5znstoou3g04&headertype=none&fp=chrome&type=tcp&sni=bgcpartners.com&sid=e6ac18b63f23#🇯🇵[openproxylist.com]": None,
    "vless://d65cc14c-f53f-4fe2-b262-97856601319c@169.40.42.16:443?security=reality&encryption=none&pbk=e2rlf57li_-mdzge9ss1bwpgp54mqrb5pfxhw2jcvvg&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=yahoo.com&sid=c39cc7310a#🇺🇸[openproxylist.com]": None,
    "vless://c124a209-d949-4951-8234-e2d918b3e6c0@185.193.89.51:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=c819rm4m_c473a8glp-ebfh8fm9o1cmeexmivdhm1fc&security=reality&sni=p.keshevoz.ru&type=tcp#🇫🇷[openproxylist.com]": None,
    "vless://564082ff-cf3c-48db-9e10-8ad2312847b4@144.31.226.178:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=tlpxtlz1y-v8b6q9mx55u6eypjfl0lcsne5zqp4yrhw&security=reality&sid=bbc68cec8bb8d2e3&sni=node16.mxvpn.dev&type=tcp#🇫🇮[openproxylist.com]": None,
    "vless://f128bc2c-8018-43a1-8ed7-66eabc8f157c@142.111.244.75:448?security=reality&encryption=none&pbk=r8ljxjo_4yluonhdkpewbd9a__xqoudwwaixx9fbcj8&headertype=none&fp=chrome&type=tcp&sni=www.samsung.com&sid=39a997621a3598c9#🇸🇪[openproxylist.com]": None,
    "trojan://nd91608427@willing-beagle.rooster465.autos:443?type=tcp&security=tls&sni=willing-beagle.rooster465.autos#🇮🇪[openproxylist.com]": None,
    "trojan://nd91608427@15.237.137.197:443?security=tls&headertype=none&fp=chrome&type=tcp&sni=fancy-skink.rooster465.autos#🇫🇷[openproxylist.com]": None,
    "trojan://nd91608427@star-kiwi.rooster465.autos:443?security=tls&headertype=none&type=tcp&sni=star-kiwi.rooster465.autos#🇫🇷[openproxylist.com]": None,
    "trojan://humanity@104.19.229.21:443?type=ws&security=tls&path=%2fassignment&host=www.calmlunch.com&sni=www.calmlunch.com#🇫🇷[openproxylist.com]": None,
    "vless://d65cc14c-f53f-4fe2-b262-97856601319c@169.40.42.95:443?security=reality&encryption=none&pbk=e2rlf57li_-mdzge9ss1bwpgp54mqrb5pfxhw2jcvvg&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=yahoo.com&sid=c39cc7310a#🇺🇸[openproxylist.com]": None,
    "vless://d65cc14c-f53f-4fe2-b262-97856601319c@169.40.42.121:443?security=reality&encryption=none&pbk=e2rlf57li_-mdzge9ss1bwpgp54mqrb5pfxhw2jcvvg&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=yahoo.com&sid=c39cc7310a#🇺🇸[openproxylist.com]": None,
    "vless://0b0915d7-6800-4580-a44b-77d84f105e6a@185.79.138.71:448?encryption=none&security=reality&sni=www.samsung.com&fp=chrome&pbk=csdgnrccwckpislfzpktik71kfpifnsotbdzkczvoh8&sid=cd21e552537c7c0b&type=tcp&headertype=none#🇫🇮[openproxylist.com]": None,
    "vless://76713d07-5a6b-49c2-abd8-bc450a2fa7fc@64.188.82.57:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=p2mv0i11jvkg-g3wfg64yvgueh0wvy6c4mtvsmpwdyq&security=reality&sid=7b1c7d9a3f2a&sni=ee-download.spectrum.vu&type=tcp#🇪🇪[openproxylist.com]": None,
    "vless://33aa2b47-484b-49f6-8f23-fb34602d221f@188.127.247.129:443?encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=kb0rdcu2kkhfnc6bsi0dmrxdej9s-mu1vvza1h1l4u4&security=reality&sid=0c&sni=yahoo.com&type=tcp#🇨🇿[openproxylist.com]": None,
    "vless://14be84e2-8b22-42c0-a1ba-3535fc8e9257@179.255.148.66:47588?security=reality&encryption=none&pbk=vii3p61px_g1qw5isp6c1zagqkqo471v9ccejwhfpe4&headertype=&fp=chrome&type=tcp&sni=yellowpages.amazon.com&sid=8b2730e4eb1313#🏳[openproxylist.com]": None,
    "vless://d65cc14c-f53f-4fe2-b262-97856601319c@169.40.42.15:443?security=reality&encryption=none&pbk=e2rlf57li_-mdzge9ss1bwpgp54mqrb5pfxhw2jcvvg&headertype=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=yahoo.com&sid=c39cc7310a#🇺🇸[openproxylist.com]": None,
    "vless://c04bf2df-2b7f-44da-a893-3792d3910fd8@89.185.80.195:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=abnwkd8cvkuimbtzgsdnsiuieni-pqukkpuinlncz2o&sid=fdda9806fe5d8584&sni=5us.skorostnet.space#🇺🇸[openproxylist.com]": None,
    "vless://f319a005-6bd0-44b3-910c-a596a2573efe@77.91.84.96:57228?encryption=none&type=tcp&security=reality&pbk=iwiq0jyyhl_yzwsbih4l4woiixbohnvmhwmgtdvf1jo&sid=6e3e0d3abe3e78a4&sni=www.googletagmanager.com&fp=chrome&flow=xtls-rprx-vision#🇫🇮[openproxylist.com]": None,
    "vless://7ce54bb3-d612-4aa7-be08-089d3c461d53@www.true.th:443?&security=tls&fp=chrome&sni=d1yxsk0zprgivr.cloudfront.net&type=ws&headertype=none&host=d1yxsk0zprgivr.cloudfront.net&path=%2f#🇹🇭[openproxylist.com]": None,
    "vless://9e3de7f7-a595-4117-b1b6-dc41eb870ab1@144.31.213.225:443?security=reality&type=tcp&pbk=abnrlkjlonyv9tofygjwwz0wn1s6sg_ycerslyku_sg&sid=d6ff9019a77e354a&sni=www.cloudflare.com&fp=chrome&flow=xtls-rprx-vision#🇬🇧[openproxylist.com]": None,
    "vless://a8e3155b-ceb1-4fcb-bc0c-2e77ec005401@88.216.220.88:443?security=reality&encryption=none&pbk=q3koyhdjmqwllyj8oikvna1btjofk45kteggaje611g&fp=firefox&type=grpc&servicename=api.v1.streamservice&sni=files.noneok.com&sid=d3b394558cfe0266#🇩🇪[openproxylist.com]": None,
    "vless://76713d07-5a6b-49c2-abd8-bc450a2fa7fc@45.145.56.163:443?security=reality&encryption=none&pbk=vci2ab6lm0ezolbj2lge-ynvakjbwoquuszmk5vcnje&headertype=&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=de2.spectrum.vu&sid=44d44d1c625a13aa#🇩🇪[openproxylist.com]": None,
    "vless://d9aa9ea3-9388-483f-a58d-a754f33ec505@gr005.bamajobin.ir:2053?mode=gun&security=reality&encryption=none&pbk=gs0dfvzx-bvkbdl2brvxsre6t2wyxxkfgp3x-mqc7by&fp=firefox&type=grpc&servicename=api.v1.data&sni=play.google.com&sid=524efc1f88592266#🇬🇧[openproxylist.com]": None,
    "vless://e99ba96d-dec8-42eb-be53-19e71eef7cab@5.253.42.164:40443?security=reality&encryption=none&pbk=g77zjbm18jeotapmvrjaxi133mzkbhku2lxhvexx8zw&headertype=none&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=deepl.com&sid=68a8#🇮🇳[openproxylist.com]": None,
    "vless://342ab7e4-5a89-0001-8809-304120d4aa83@95.85.224.51:443?encryption=none&flow=xtls-rprx-vision&type=tcp&security=reality&sni=max.ru&fp=qq&pbk=wweahwuvd-phmnjnj823cer0c4cmibes08ahsuezmdc&sid=a696de84963656de#🇪🇪[openproxylist.com]": None,
    "vless://c8dcbe44-5714-4f99-8d7a-aadebea34abf@91.103.140.243:443?encryption=none&fp=firefox&pbk=118rmk41g_0beoqdr2v_1f8abzc1wkxdolze-lxqowm&security=reality&sid=bff835c98c&sni=www.amd.com&spx=%2fdosqm9da3rf8ag2&type=tcp#🇫🇮[openproxylist.com]": None,
    "vless://ab7d5ea9-6eca-47c3-b14b-67378fc2d7c2@152.53.114.186:443?encryption=none&flow=xtls-rprx-vision&fp=chrome&pbk=uo3eobgu3xurhigee0gfcn5zoz8yxncwww6zayzd3sa&security=reality&sid=4e9b0c2d1a3f5768&sni=as.tunnelx.space&type=tcp#🇦🇹[openproxylist.com]": None,
    "vless://69a74770-7152-4a27-bef0-2615ca16e1b1@77.233.214.116:40443?encryption=none&flow=xtls-rprx-vision&pbk=d0aqp0cwaqr55q-zpwp6__axn9cot9nezj0uzlnclck&type=tcp&sid=bd72&security=reality&headertype=none&sni=deepl.com&fp=chrome#🇳🇱[openproxylist.com]": None,
    "vless://9150748b-fa2b-4ef1-a7f1-7c4a76e2dc0b@update.netraidly.ru:40443?encryption=none&type=tcp&security=reality&headertype=none&sni=deepl.com&fp=qq&pbk=u1abwltij71fw63nwmukzbezsqkadibrukcatinuxuw&sid=27bb&flow=xtls-rprx-vision#🇳🇱[openproxylist.com]": None,
    "vless://c04bf2df-2b7f-44da-a893-3792d3910fd8@78.17.208.22:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=abnwkd8cvkuimbtzgsdnsiuieni-pqukkpuinlncz2o&security=reality&sid=fdda9806fe5d8584&sni=fr05.skorostnet.space&type=tcp#🇫🇷[openproxylist.com]": None,
    "trojan://nd91608427@gentle-raptor.rooster465.autos:443?type=tcp&security=tls&sni=gentle-raptor.rooster465.autos#🇩🇪[openproxylist.com]": None,
    "vless://c1c04450-bf71-4049-ad0c-9cf6d94d9f1f@60.248.219.78:443?&security=tls&sni=ty986gfazs.cainiaohub.xyz&type=ws&headertype=none&host=ty986gfazs.cainiaohub.xyz&path=%2f81574b6b-c9d7-44a0-b83d-dad56e8cb530#🇹🇼[openproxylist.com]": None,
    "vless://ab7d5ea9-6eca-47c3-b14b-67378fc2d7c2@152.53.114.186:443?type=tcp&security=reality&encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=uo3eobgu3xurhigee0gfcn5zoz8yxncwww6zayzd3sa&sid=4e9b0c2d1a3f5768&sni=as.tunnelx.space#🇦🇹[openproxylist.com]": None,
}

if __name__ == "__main__":
    asyncio.run(main())
