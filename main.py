from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


def _parse_ipv4(ip: str) -> int:
    """Validate and convert an IPv4 dotted-decimal string to a 32-bit int."""
    if not isinstance(ip, str) or not ip:
        raise ValueError("Alamat IP tidak boleh kosong")

    if " " in ip:
        raise ValueError("Alamat IP tidak boleh mengandung spasi")

    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError("Alamat IP harus tepat 4 oktet")

    octets = []
    for part in parts:
        if not part:
            raise ValueError("Oktet tidak boleh kosong")
        if not part.isdigit():
            raise ValueError("Oktet harus berupa angka")
        if len(part) > 1 and part[0] == "0":
            raise ValueError("Angka nol di depan tidak diperbolehkan")
        value = int(part)
        if not 0 <= value <= 255:
            raise ValueError("Tiap oktet harus bernilai antara 0 sampai 255")
        octets.append(value)

    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]


def _parse_prefix(prefix: Any) -> int:
    """Validate a CIDR prefix and return it as an int in range 0..32."""
    if isinstance(prefix, bool) or not isinstance(prefix, int):
        raise ValueError("Prefix harus berupa bilangan bulat")
    if not 0 <= prefix <= 32:
        raise ValueError("Prefix harus berada dalam rentang 0-32")
    return prefix


def _int_to_ipv4(value: int) -> str:
    return ".".join(str((value >> shift) & 0xFF) for shift in (24, 16, 8, 0))


def _mask_from_prefix(prefix: int) -> int:
    if prefix == 0:
        return 0
    return (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF


def hitung_subnet(ip: str, prefix: int) -> dict:
    ip_int = _parse_ipv4(ip)
    prefix = _parse_prefix(prefix)

    mask_int = _mask_from_prefix(prefix)
    network_int = ip_int & mask_int
    host_bits = 32 - prefix

    if prefix == 32:
        network_int = ip_int
        broadcast = None
        first_host = last_host = _int_to_ipv4(ip_int)
        usable_hosts = 1
    elif prefix == 31:
        broadcast = None
        first_host = _int_to_ipv4(network_int)
        last_host = _int_to_ipv4(network_int + 1)
        usable_hosts = 2
    else:
        broadcast_int = network_int | ((1 << host_bits) - 1)
        first_host = _int_to_ipv4(network_int + 1)
        last_host = _int_to_ipv4(broadcast_int - 1)
        broadcast = _int_to_ipv4(broadcast_int)
        usable_hosts = (1 << host_bits) - 2

    return {
        "mask": _int_to_ipv4(mask_int),
        "network": _int_to_ipv4(network_int),
        "broadcast": broadcast,
        "first_host": first_host,
        "last_host": last_host,
        "usable_hosts": usable_hosts,
    }


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    if not isinstance(kebutuhan_host, list) or len(kebutuhan_host) == 0:
        raise ValueError("Daftar kebutuhan host kosong")

    for k in kebutuhan_host:
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError("Kebutuhan host harus berupa bilangan bulat >= 1")

    if not isinstance(network_cidr, str) or "/" not in network_cidr:
        raise ValueError("network_cidr harus dalam format IP/prefix")

    ip, prefix_str = network_cidr.split("/", 1)
    if not prefix_str.isdigit():
        raise ValueError("Prefix harus berupa bilangan bulat antara 0 dan 32")
    prefix = _parse_prefix(int(prefix_str))

    ip_int = _parse_ipv4(ip)
    mask_int = _mask_from_prefix(prefix)
    network_int = ip_int & mask_int

    if network_int != ip_int:
        raise ValueError("network_cidr bukan alamat jaringan yang valid (host bit aktif)")

    block_size = 1 << (32 - prefix)
    sorted_kebutuhan = sorted(kebutuhan_host, reverse=True)

    results = []
    cursor = network_int

    for kebutuhan in sorted_kebutuhan:
        size = 4
        while size < kebutuhan + 2:
            size *= 2

        block_prefix = 32 - (size.bit_length() - 1)
        if block_prefix < prefix or cursor + size > network_int + block_size:
            raise ValueError("Total ruang alamat tidak cukup menampung seluruh kebutuhan")

        subnet = hitung_subnet(_int_to_ipv4(cursor), block_prefix)
        subnet["kebutuhan"] = kebutuhan
        subnet["network_cidr"] = f"{subnet['network']}/{block_prefix}"

        results.append(subnet)
        cursor += size

    return results


@app.get("/", response_class=HTMLResponse)
def read_index():
    index_path = Path(__file__).parent / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html tidak ditemukan")
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/api/subnet")
def api_subnet(ip: str = Query(default=""), prefix: Any = Query(default=None)):
    try:
        if prefix is None or prefix == "":
            raise ValueError("Prefix harus diisi")
        try:
            prefix_val = int(prefix)
        except (ValueError, TypeError):
            raise ValueError("Prefix harus berupa bilangan bulat")
        return hitung_subnet(ip, prefix_val)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/vlsm")
def api_vlsm(payload: dict):
    network = payload.get("network", "")
    kebutuhan_host = payload.get("kebutuhan_host", [])
    try:
        return alokasi_vlsm(network, kebutuhan_host)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
