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


# Create SSL context ONCE with session reuse
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE  # Skport cert validation for speed
DEFAULT_TIMEOUT = 50


max_ping = 5000


trasport_layer = ["type=ws", "type=tcp", "type=grpc", "type=xhttp"]

security_layer: list = ["security=reality", "security=tls"]


def decode_base64(data):
    if not data or not isinstance(data, str):
        return False

    try:
        # data = data.strip()
        # Convert URL-safe base64 characters to standard base64
        data = data.replace("_", "/").replace("-", "+")

        # Fix missing Base64 padding
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)

        # validate=True ensures non-base64 input raises an error instead of returning garbage
        decoded_bytes = base64.b64decode(data)

        # Decode UTF-8 cleanly with error handling
        return decoded_bytes.decode("utf-8")

    except Exception as error:
        print(error)
        return False


def encode_base64(data):
    try:
        if isinstance(data, str):
            data = data.encode("utf-8")
        encoded = base64.b64encode(data).decode("utf-8")
        return encoded.replace("/", "_").replace("+", "-").rstrip("=")
    except Exception:
        return False


def remove_allow_insecure(url: str) -> str:
    # First, handle the case where it's the first parameter: ?allowInsecure=val& or ?insecure=val&
    url = re.sub(r"\?(?:allowInsecure|insecure)=[^&#]*&", "?", url, flags=re.IGNORECASE)

    # Then, remove it from middle or end: &allowInsecure=val or &insecure=val
    url = re.sub(r"&(?:allowInsecure|insecure)=[^&#]*", "", url, flags=re.IGNORECASE)

    # Finally, handle the case where it's the only parameter: ?allowInsecure=val or ?insecure=val
    url = re.sub(
        r"\?(?:allowInsceure|insecure)=[^&#]*(?=#|$)", "", url, flags=re.IGNORECASE
    )

    return url

    return url


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
            if text:
                return True, response_time

            else:
                return False, None

    except Exception:
        # Silently ignore connection errors, timeouts, etc.
        return False, None

    except asyncio.TimeoutError:
        return False, None

    except aiohttp.ClientError as e:
        return False, None

    except asyncio.CancelledError:
        # ✅ Handle cancellation gracefully
        return False, None


async def fetch_sub(url: str) -> str:
    resolver = AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])

    connector = aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,  # Reuse SSL context
        limit=20,  # Total connections
        force_close=True,  # Close connections after each request
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


async def ping_multiple_async(hosts_ports, max_concurrent=50):
    semaphore = asyncio.Semaphore(max_concurrent)

    resolver = AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])
    connector = aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,  # Reuse SSL context
        force_close=True,  # Close connections after each request
        resolver=resolver,
    )
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)

    async def limited_ping(host):
        async with semaphore:
            async with aiohttp.ClientSession(
                connector=connector, timeout=timeout
            ) as session:
                return await CheckUrl(session, host)

    tasks = [limited_ping(host) for host in hosts_ports]
    return await asyncio.gather(*tasks)


def parse_data(data: list):
    parsed: dict = {}
    decodded = ""
    host = ""

    ip: str = ""
    port: str = ""
    host_path: str = ""

    trasport_layer: list = ["type=ws", "type=tcp", "type=grpc", "type=xhttp"]
    security_layer: list = ["security=reality", "security=tls"]

    for url in data:
        try:
            if any(security in url for security in security_layer):
                url = url.lower()
                url = remove_allow_insecure(url)

                if "type=ws" in url:
                    parsed_url = urlparse(url)

                    # Fix query string - replace HTML entities
                    query = parsed_url.query
                    query = query.replace("&amp;", "&")
                    query = query.replace("&lt;", "<")
                    query = query.replace("&gt;", ">")
                    query = query.replace("&quot;", '"')

                    # Parse query parameters into a dictionary
                    params = parse_qs(query, keep_blank_values=True)

                    ip_port = (
                        parsed_url.netloc.split("@")[-1]
                        if "@" in parsed_url.netloc
                        else parsed_url.netloc
                    )
                    if ":" in ip_port:
                        ip, port = ip_port.rsplit(":", 1)
                    else:
                        continue

                    # Extract host and path
                    if "host" in params and params["host"]:
                        host = params.get("host", [None])[0]
                    else:
                        host = ip

                    if "path" in params and params["path"]:
                        raw_path = params.get("path", [None])[0]
                        path = unquote(raw_path) if raw_path is not None else None
                    else:
                        path = ""

                    host_path = "https://" + host + path

                    if host_path:
                        parsed[url] = host_path

                elif "type=tcp" in url:
                    parsed_url = urlparse(url)

                    # 1. Extract IP:Port from netloc (104.17.19.109:2083)
                    ip_port = (
                        parsed_url.netloc.split("@")[-1]
                        if "@" in parsed_url.netloc
                        else parsed_url.netloc
                    )
                    if ":" in ip_port:
                        ip, port = ip_port.rsplit(":", 1)
                    else:
                        continue

                    host_path = "https://" + ip

                    if ip_port:
                        parsed[url] = host_path

                elif "type=grpc" in url:
                    parsed_url = urlparse(url)

                    # Fix query string - replace HTML entities
                    query = parsed_url.query
                    query = query.replace("&amp;", "&")
                    query = query.replace("&lt;", "<")
                    query = query.replace("&gt;", ">")
                    query = query.replace("&quot;", '"')

                    # Parse query parameters into a dictionary
                    params = parse_qs(query, keep_blank_values=True)

                    # print(parsed_url)

                    ip_port = (
                        parsed_url.netloc.split("@")[-1]
                        if "@" in parsed_url.netloc
                        else parsed_url.netloc
                    )
                    if ":" in ip_port:
                        ip, port = ip_port.rsplit(":", 1)
                    else:
                        continue

                    # Extract host and path
                    if "path" in params and params["path"]:
                        raw_path = params.get("path", [None])[0]
                        path = unquote(raw_path) if raw_path is not None else None
                    else:
                        path = ""

                    host_path = "https://" + ip + path

                    if host_path:
                        parsed[url] = host_path

                elif "type=xhttp" in url:
                    parsed_url = urlparse(url)

                    # Fix query string - replace HTML entities
                    query = parsed_url.query
                    query = query.replace("&amp;", "&")
                    query = query.replace("&lt;", "<")
                    query = query.replace("&gt;", ">")
                    query = query.replace("&quot;", '"')

                    # Parse query parameters into a dictionary
                    params = parse_qs(query, keep_blank_values=True)

                    ip_port = (
                        parsed_url.netloc.split("@")[-1]
                        if "@" in parsed_url.netloc
                        else parsed_url.netloc
                    )
                    if ":" in ip_port:
                        ip, port = ip_port.rsplit(":", 1)
                    else:
                        continue

                    # Extract host and path
                    if "host" in params and params["host"]:
                        host = params.get("host", [None])[0]
                    else:
                        host = ip

                    if "path" in params and params["path"]:
                        raw_path = params.get("path", [None])[0]
                        path = unquote(raw_path) if raw_path is not None else None
                    else:
                        path = ""

                    host_path = "https://" + host + path

                    if host_path:
                        parsed[url] = host_path

        except Exception as e:
            print(e)
    return parsed


async def save_configs(file_path: str, urls: list):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for url in urls.items():
                file.write(f"{encode_base64(url)}\n")
    except Exception as error:
        print("file saveing operation is faild, error code:" + str(error))


async def main():
    project_dir = pathlib.Path(__file__).parent
    subresources_path = pathlib.Path.joinpath(project_dir, "Resources", "subs.txt")
    normalconfig_path = pathlib.Path.joinpath(
        project_dir, "Configs", "tcp_pass", "normal.txt"
    )
    SNISpoofing_path = pathlib.Path.joinpath(
        project_dir, "Configs", "tcp_pass", "SNI_Spoofing.txt"
    )

    sub_urls: str = ""
    fetched_sub: str = ""
    found: list = []

    urls = []
    OkUrls = []
    parsed_configs = []
    configs = {}

    # XHTTP
    # vless://%40V2XNET@127.0.0.1:40443?encryption=mlkem768x25519plus.native.0rtt.BBBQ6KZyjiYmpp2ErhKd0OwCBOm4J6_McyVQdB5yhBI&security=tls&sni=butimcreepimweirdo.dpdns.org&fp=chrome&alpn=h2%2Chttp%2F1.1&insecure=0&allowInsecure=0&type=xhttp&host=butimcreepimweirdo.dpdns.org&path=%2F&mode=auto&extra=%7B%22mode%22%3A%22auto%22%2C%22xPaddingBytes%22%3A%22100-1000%22%7D#ping%3A5
    # vless://3e37ef76-835d-4ad2-a1d3-414ef90532bf@127.0.0.1:40443?encryption=none&security=tls&sni=accounts.fastly.com&fp=chrome&alpn=h3&insecure=0&allowInsecure=0&type=xhttp&host=ovd13.global.ssl.fastly.net&path=%2F&mode=packet-up#ping%3A5
    # vless://2ce77806-5bc3-45ea-82d0-d7101284dd9f@104.18.151.14:2087?encryption=none&security=tls&sni=8.mobilezahra.com&fp=chrome&alpn=h3%2Ch2%2Chttp%2F1.1&insecure=0&allowInsecure=0&type=xhttp&host=8.mobilezahra.com&path=%2F&mode=auto#ping%3A9
    # vless://885417a5-b568-4299-bde4-db01b654ebed@104.18.151.14:2087?encryption=none&security=tls&sni=2.mobilezahra.com&fp=chrome&alpn=h3%2Ch2%2Chttp%2F1.1&insecure=0&allowInsecure=0&type=xhttp&host=2.mobilezahra.com&path=%2F&mode=auto#ping%3A13

    # TCP / RAW
    # vless://c04bf2df-2b7f-44da-a893-3792d3910fd8@185.212.119.177:443?encryption=none&security=none&type=tcp&headerType=none#%F0%9F%87%AB%F0%9F%87%AE%5Bopenproxylist.com%5D%20vless-FI
    # vless://342ab7e4-5a89-0001-8809-304120d4aa83@95.85.224.51:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=max.ru&fp=qq&pbk=WWeAHWUVD-phmnjNJ823cer0c4CMIbEs08AhsuEZmDc&sid=a696de84963656de&type=tcp&headerType=none#%F0%9F%8F%B3%5Bopenproxylist.com%5D%20vless-

    # GRCP
    # vless://d9aa9ea3-9388-483f-a58d-a754f33ec505@gr005.bamajobin.ir:2053?encryption=none&security=reality&sni=play.google.com&fp=firefox&pbk=GS0dfvzX-bVKBDl2brVxsrE6T2WyXXkfgP3x-mQC7BY&sid=524efc1f88592266&type=grpc&authority=&serviceName=api.v1.data&mode=gun#%F0%9F%87%AC%F0%9F%87%A7%5Bopenproxylist.com%5D%20vless-GB
    # vless://a8e3155b-ceb1-4fcb-bc0c-2e77ec005401@88.216.220.87:443?encryption=none&security=reality&sni=api.noneok.com&fp=firefox&pbk=S8O8R938N960cpQfIIDXsJTxeGAkbVv6PlIqP0-d30w&sid=1ea59febb8d4fc8e&type=grpc&authority=&serviceName=api.v1.StreamService&mode=gun#%F0%9F%8F%B3%5Bopenproxylist.com%5D%20vless-
    # vless://a8e3155b-ceb1-4fcb-bc0c-2e77ec005401@88.216.220.88:443?encryption=none&security=reality&sni=files.noneok.com&fp=chrome&pbk=q3kOYHdjmqWLLYj8oikvna1bTjofk45ktegGaJE611g&sid=d3b394558cfe0266&type=grpc&authority=&serviceName=api.v1.StreamService&mode=gun#%F0%9F%87%A9%F0%9F%87%AA%5Bopenproxylist.com%5D%20vless-DE
    # vless://d9aa9ea3-9388-483f-a58d-a754f33ec505@gr005.bamajobin.ir:2053?encryption=none&security=reality&sni=play.google.com&fp=firefox&pbk=GS0dfvzX-bVKBDl2brVxsrE6T2WyXXkfgP3x-mQC7BY&sid=524efc1f88592266&type=grpc&authority=&serviceName=api.v1.data&mode=gun#%F0%9F%87%AC%F0%9F%87%A7%5Bopenproxylist.com%5D%20vless-GB

    # WS
    # vless://435bda4c-fe5e-42c9-a3ad-15334943b38a@104.18.37.90:80?encryption=none&security=none&type=ws&host=us3.rtacg.com&path=%2F#ping%3A10
    # vless://fdb12587-1c15-4883-8d7a-9894641e183c@104.17.19.109:2083?encryption=none&security=tls&sni=nova-mango-vault-2e63.wolf-fbi-red.workers.dev&fp=random&insecure=0&allowInsecure=0&type=ws&host=nova-mango-vault-2e63.wolf-fbi-red.workers.dev&path=%2F%3Fu%3D3e3fff3b5b#ping%3A14

    # Loading sub urls file to urls
    with open(file=subresources_path, mode="r", encoding="utf-8") as file:
        # sub_urls = file.readlines()
        sub_urls = file.read().splitlines()

    print(sub_urls)
    for url in sub_urls:
        # fetch the config to "fetched_sub" in fourm of str
        fetched_sub = await fetch_sub(url)

        if fetched_sub:
            found = re.findall(r"(?:vless|trojan)://[^\s]+", fetched_sub)

            if not found:
                fetched_sub = decode_base64(fetched_sub)

                found = re.findall(r"(?:vless|trojan)://[^\s]+", fetched_sub)

            for link in found:
                link = link.replace("&amp;", "&")
                link = link.replace("&lt;", "<")
                link = link.replace("&gt;", ">")
                link = link.replace("&quot;", '"')
                urls.append(link)

        configs = parse_data(urls)

    print("Found configs:", len(configs))

    hosts = []

    for url in configs.values():
        hosts.append(url)

    results = await ping_multiple_async(hosts)

    found = dict(zip(configs, results))

    config = {}
    
    print(results)
    

    for url in found.items():
        if url[1][0]:
            if url[1][1] < max_ping:
                config[re.sub(r"#.*$", f"#ping:{str(int(url[1][1]))}", url[0])] = url[1]

    print("working configs:", len(config))

    found = dict(sorted(config.items(), key=lambda item: item[1][1]))

    found = dict(list(found.items())[:100])

    print("working configs:", len(found))

    with open(normalconfig_path, "w", encoding="utf-8") as file:
        for url in found.items():
            file.write(f"{url[0]}\n")


if __name__ == "__main__":
    asyncio.run(main())
