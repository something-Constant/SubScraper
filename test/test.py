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
import aiodns


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



import asyncio
import socket
import aiodns

async def resolve_host(hostname):
    resolver = aiodns.DNSResolver(nameservers=["8.8.8.8", "1.1.1.1"])
    try:
        result = await resolver.getaddrinfo(hostname, socket.AF_INET)
        # Access the 'host' attribute directly from each AddrInfoNode
        ips = [node.host for node in result.nodes]
        return ips
    except aiodns.error.DNSError as e:
        print(f"DNS Resolution error: {e}")
        return []
    except Exception as e:
        print(f"Failed to resolve: {e}")
        return []
        
async def get_ipinfo(ip):
    resolver = AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])

    connector = aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,  # Reuse SSL context
        limit=200,  # Total connections
        force_close=True,  # Close connections after each request
        resolver=resolver,
    )
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)

    try:
        async with aiohttp.ClientSession(
            connector=connector, timeout=timeout
        ) as session:
            async with session.get(
                f"https://api.ip.sb/geoip/{ip}",
                ssl=SSL_CONTEXT,
                allow_redirects=True,
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    # Try to get country name or code
                    country = data.get("country") or data.get("country_code")
                    isp = data.get("isp")

                    if country:
                        # print(f"Country: {country}, isp: {isp}")
                        return country, isp

                    return False

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        # pass
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

    data = await resolve_host("sync.watchwave.link")
    print(data)
    
    data = await get_ipinfo("sync.watchwave.link")

    print(data)


if __name__ == "__main__":
    asyncio.run(main())
