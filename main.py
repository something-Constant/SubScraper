import re
import asyncio
import aiohttp
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
DEFAULT_TIMEOUT = 5


def build_connector(limit: int = 20, force_close: bool = True):
    """Use the system DNS resolver by default to avoid CI DNS outages.

    Hardcoded public nameservers like 8.8.8.8/1.1.1.1 can fail in GitHub Actions
    with "DNS server returned general failure" even when the rest of the network
    is working. Let aiohttp use the platform resolver instead.
    """
    return aiohttp.TCPConnector(
        ssl=SSL_CONTEXT,
        limit=limit,
        force_close=force_close,
    )


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
        return ""


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
    connector = build_connector(limit=200, force_close=True)
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
                        print(f"Country: {country}, isp: {isp}")
                        return country, isp

                    return False

    except Exception:
        return False


def text_qrcode(name, data, location=None):
    ### check if root foleder exist
    if location:
        if not pathlib.Path(location).exists():
            os.mkdir(location)
    else:
        location = pathlib.Path(__file__).parent / "qrcode"
        if not pathlib.Path(location).exists():
            os.mkdir(location)

    location = pathlib.Path.joinpath(location, name)

    img = qrcode.make(data)
    type(img)  # qrcode.image.pil.PilImage
    img.save(location)


async def fetch_sub(url: str) -> str:
    connector = build_connector(limit=20, force_close=True)
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


async def tcping_async(host: str, timeout: float = 1) -> Tuple[bool, Optional[float]]:
    """Async TCP ping using asyncio"""
    start_time = time.time()
    port = 0
    try:
        async with asyncio.timeout(timeout):
            # Modern asyncio.open_connection (no loop parameter)
            reader, writer = await asyncio.open_connection(host, 443, ssl=False)

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


async def ping_multiple_async(hosts_ports, max_concurrent=50):
    semaphore = asyncio.Semaphore(max_concurrent)

    connector = build_connector(limit=10, force_close=True)
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
    ) as session:

        async def limited_ping(host):
            async with semaphore:
                return await CheckUrl(session, host)
            # return await tcping_async(host)

        tasks = [limited_ping(host) for host in hosts_ports]
        return await asyncio.gather(*tasks)


def convert_to_sppof(data: str):
    try:
        pattern = r"(@)(?:\[[0-9a-fA-F:]+\]|[^:/#?]+)(?::\d+)?"
        replacement = r"\g<1>127.0.0.1:40443"
        return re.sub(pattern, replacement, data)

    except Exception as e:
        print(e)


async def main():
    project_dir = pathlib.Path(__file__).parent
    subresources_path = pathlib.Path.joinpath(project_dir, "Resources", "subs.txt")
    nomralconfig_path = pathlib.Path.joinpath(
        project_dir, "Configs", "tcp_pass", "normal.txt"
    )
    SNISpoofing_path = pathlib.Path.joinpath(
        project_dir, "Configs", "tcp_pass", "SNI_Spoofing.txt"
    )

    tcp_pass_normal_github: str = "https://github.com/something-Constant/SubScraper/raw/refs/heads/main/Configs/tcp_pass/normal.txt"
    tcp_pass_spoof_github: str = "https://github.com/something-Constant/SubScraper/raw/refs/heads/main/Configs/tcp_pass/SNI_Spoofing.txt"

    sub_urls: str = ""
    fetched_sub: str = ""
    found: list = []
    urls = []
    parsed_configs = []

    # Loading sub urls file to urls
    with open(file=subresources_path, mode="r", encoding="utf-8") as file:
        sub_urls = file.read().splitlines()

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

    parsed_configs = parse_data(urls)
    print("Found configs:", len(parsed_configs))

    if not parsed_configs:
        print("No configs found.")
        return

    # 4. Test them
    hosts = list(parsed_configs.values())
    results = await ping_multiple_async(hosts)

    good = {}
    temp = {}
    sorted_good = {}

    good = dict(zip(parsed_configs, results))

    for url in good.items():
        if url[1][0]:
            if url[1][1] < max_ping:
                temp[re.sub(r"#.*$", f"#ping:{str(int(url[1][1]))}", url[0])] = url[1]

    sorted_good = dict(sorted(temp.items(), key=lambda item: item[1][1])[:200])

    print("working configs:", len(sorted_good))

    with open(nomralconfig_path, "w", encoding="utf-8") as file:
        for link in sorted_good:
            file.write(link + "\n")

    with open(SNISpoofing_path, "w", encoding="utf-8") as file:
        for link in sorted_good:
            file.write(convert_to_sppof(link) + "\n")

    text_qrcode("tcp_pass_normal.png", tcp_pass_normal_github)
    text_qrcode("tcp_pass_spoof.png", tcp_pass_spoof_github)


if __name__ == "__main__":
    asyncio.run(main())
