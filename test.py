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
DEFAULT_TIMEOUT = 20


max_ping = 400


trasport_layer = ["type=ws", "type=tcp", "type=grpc", "type=xhttp"]

security_layer: list = ["security=reality", "security=tls"]


async def CheckUrl(session: aiohttp.ClientSession, Url: str):
    try:
        start_time = time.time()

        async with session.get(
            Url,
            ssl=SSL_CONTEXT,
            allow_redirects=True,
        ) as response:
            response_time = int((time.time() - start_time) * 1000)

            if response.status == 200 and response.text():
                return True, response_time

            else:
                return False

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        pass

    return False


async def main():
    sub_resources = pathlib.Path.joinpath(project_dir, "/Resources/subs.txt")
    normal_config = pathlib.Path.joinpath(project_dir, "/Configs/tcp_pass/normal.txt")
    SNI_Spoofing = pathlib.Path.joinpath(
        project_dir, "/Configs/tcp_pass/SNI_Spoofing.txt"
    )

    sub_urls: str = ""
    fetched_sub: str = ""
    found: list = []

    urls = []
    OkUrls = []
    parsed_configs = []
    configs = []

    resolver = AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])

    connector = aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,  # Reuse SSL context
        limit=200,  # Total connections
        force_close=True,  # Close connections after each request
        resolver=resolver,
    )
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)

    
    async with aiohttp.ClientSession(
        connector=connector, timeout=timeout
    ) as session:
        text = CheckUrl(session,"https://vod.ensf.top/api/v1/irc")
    
    print(text)
if __name__ == "__main__":
    asyncio.run(main())
