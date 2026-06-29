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


# Create SSL context ONCE with session reuse
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE  # Skport cert validation for speed

DEFAULT_TIMEOUT = 20
max_ping = 400

urls = []
Url = ""
OkUrls = []
configs = []
found = []
configs = []


project_dir = pathlib.Path(__file__).parent


def decode_base64(data):
    try:
        data = data.replace("_", "/").replace("-", "+")
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)
        return base64.b64decode(data).decode("utf-8")
    except Exception:
        return False


def text_qrcode(name, data, location=None):
    ### check if root foleder exist
    if location:
        if not pathlib.Path(location).exists():
            os.mkdir(location)
    else:
        location = pathlib.Path(__file__).parent / "Qrcode"
        if not pathlib.Path(location).exists():
            os.mkdir(location)

    location = pathlib.Path.joinpath(location, name)

    img = qrcode.make(data)
    type(img)  # qrcode.image.pil.PilImage
    img.save(location)


async def CheckUrl(session: aiohttp.ClientSession, Url: str):
    try:
        async with session.get(
            Url,
            ssl=SSL_CONTEXT,
            allow_redirects=True,
        ) as response:
            if response.status == 200:
                return Url

            else:
                return False

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        pass

    return False


async def fetch_sub(url: str):
    resolver = AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])

    connector = aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,  # Reuse SSL context
        limit=20,  # Total connections
        # force_close=True,  # Close connections after each request
        resolver=resolver,
    )
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)

    try:
        async with aiohttp.ClientSession(
            connector=connector, timeout=timeout
        ) as session:
            async with session.get(
                url,
                ssl=SSL_CONTEXT,
                allow_redirects=True,
            ) as response:
                if response.status == 200:
                    return await response.text()

                else:
                    return False

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        pass

    return False


async def tcping_async(
    host: str, port: int, timeout: float = 1
) -> Tuple[bool, Optional[float]]:
    """Async TCP ping using asyncio"""
    start_time = time.time()

    try:
        async with asyncio.timeout(timeout):
            # Modern asyncio.open_connection (no loop parameter)
            reader, writer = await asyncio.open_connection(host, port, ssl=False)

            writer.close()
            await writer.wait_closed()

            response_time = int((time.time() - start_time) * 1000)
            return True, response_time

    except asyncio.TimeoutError:
        return False, None
    except ConnectionRefusedError:
        return False, None
    except socket.gaierror:
        return False, None
    except Exception as e:
        # Log unexpected errors for debugging
        print(f"Unexpected error connecting to {host}:{port} - {e}")
        return False, None


async def ping_multiple_async(hosts_ports: List[Tuple[str, int]], max_concurrent=50):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_ping(host, port):
        async with semaphore:
            return await tcping_async(host, port)

    tasks = [limited_ping(host, port) for host, port in hosts_ports]
    return await asyncio.gather(*tasks)


def parse_data(data: list):
    parsed = {}
    decodded = ""
    host = ""
    port = ""

    for url in data:
        try:
            if url.find("trojan://"):
                decodded = decode_base64(re.sub(r"^(trojan://)", "", url))

                host = url[(url.find("@") + 1) : url.find("?")].split(":")

                if len(host) <= 1:
                    continue

                port = host[1]
                host = host[0]

                if decodded:
                    parsed[url] = (host, port)

                else:
                    parsed[url] = (host, port)

            if url.find("vless://"):
                decodded = decode_base64(re.sub(r"^(trojan://)", "", url))

                host = url[(url.find("@") + 1) : url.find("?")].split(":")
                if len(host) <= 1:
                    continue

                port = host[1]
                host = host[0]

                if decodded:
                    parsed[url] = (host, port)

                else:
                    parsed[url] = (host, port)

        except Exception as e:
            print(e)

    return parsed


# Meybe in the next updait
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
                    country = await response.json()
                    if country["country"]:
                        country = country["country"]
                        print(f"Country: {country}")
                        return country
                    return False
                return False

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        pass

    return False


async def main():
    # url_file = pathlib.Path.joinpath(project_dir, "/Resources/urls_test.txt")
    url_file = project_dir / "Resources" / "urls_test.txt"

    with open(file="urls_test.txt", mode="r", encoding="utf-8") as file:
        urls = file.readlines()

    for url in urls:
        fetched_sub = await fetch_sub(url)

        if fetched_sub:
            found = re.findall(r"(?:vless|trojan)://[^\s]+", fetched_sub)

            if not found:
                fetched_sub = decode_base64(fetched_sub)
                found = re.findall(r"(?:vless|trojan)://[^\s]+", fetched_sub)

            configs.extend(found)

    print("Found configs:", len(configs))

    found = parse_data(configs)

    hosts = []

    for url in found.values():
        hosts.append(url)

    results = await ping_multiple_async(hosts)

    found = dict(zip(found, results))

    config = {}

    for url in found.items():
        if url[1][0] and url[1][1] < max_ping:
            config[re.sub(r"#.*$", f"#ping:{str(int(url[1][1]))}", url[0])] = url[1]

    print("working configs:", len(config))

    found = dict(sorted(config.items(), key=lambda item: item[1][1]))

    found = dict(list(found.items())[:100])

    print("working configs:", len(found))

    with open("test.txt", "w", encoding="utf-8") as file:
        for url in found.items():
            file.write(f"{url[0]}\n")


if __name__ == "__main__":
    asyncio.run(main())
