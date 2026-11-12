import pytest
from fastapi.testclient import TestClient

from main import app, hitung_subnet

client = TestClient(app)


# --- Subnet: Kasus Normal & Edge Cases --------------------------------------

@pytest.mark.parametrize(
    "ip, prefix, expected",
    [
        # Kasus Normal
        (
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "10.0.0.0",
            30,
            {
                "mask": "255.255.255.252",
                "network": "10.0.0.0",
                "broadcast": "10.0.0.3",
                "first_host": "10.0.0.1",
                "last_host": "10.0.0.2",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.1",
            24,
            {
                "mask": "255.255.255.0",
                "network": "192.168.1.0",
                "broadcast": "192.168.1.255",
                "first_host": "192.168.1.1",
                "last_host": "192.168.1.254",
                "usable_hosts": 254,
            },
        ),
        (
            "10.0.0.0",
            8,
            {
                "mask": "255.0.0.0",
                "network": "10.0.0.0",
                "broadcast": "10.255.255.255",
                "first_host": "10.0.0.1",
                "last_host": "10.255.255.254",
                "usable_hosts": 16777214,
            },
        ),
        # Edge Cases
        (
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
        (
            "0.0.0.0",
            0,
            {
                "mask": "0.0.0.0",
                "network": "0.0.0.0",
                "broadcast": "255.255.255.255",
                "first_host": "0.0.0.1",
                "last_host": "255.255.255.254",
                "usable_hosts": 4294967294,
            },
        ),
    ],
)
def test_hitung_subnet_sukses(ip, prefix, expected):
    result = hitung_subnet(ip, prefix)
    assert result["mask"] == expected["mask"]
    assert result["network"] == expected["network"]
    assert result["broadcast"] == expected["broadcast"]
    assert result["first_host"] == expected["first_host"]
    assert result["last_host"] == expected["last_host"]
    assert result["usable_hosts"] == expected["usable_hosts"]


# --- Subnet: Input Tidak Valid ----------------------------------------------

@pytest.mark.parametrize(
    "ip, prefix",
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1", 24),
        ("abc", 24),
        ("", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
        ("192.168.1.1 ", 24),
    ],
)
def test_hitung_subnet_invalid(ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


# --- API: GET /api/subnet (Sukses) ------------------------------------------

def test_api_subnet_sukses():
    response = client.get("/api/subnet", params={"ip": "172.16.5.130", "prefix": 25})
    assert response.status_code == 200
    body = response.json()
    assert body["mask"] == "255.255.255.128"
    assert body["network"] == "172.16.5.128"
    assert body["broadcast"] == "172.16.5.255"
    assert body["first_host"] == "172.16.5.129"
    assert body["last_host"] == "172.16.5.254"
    assert body["usable_hosts"] == 126


# --- API: GET /api/subnet (Input Tidak Valid) --------------------------------

@pytest.mark.parametrize(
    "ip, prefix",
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1", 24),
        ("abc", 24),
        ("", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
        ("192.168.1.1 ", 24),
    ],
)
def test_api_subnet_invalid(ip, prefix):
    response = client.get("/api/subnet", params={"ip": ip, "prefix": prefix})
    assert response.status_code == 400
    assert "detail" in response.json()


# --- API: GET / -------------------------------------------------------------

def test_root_mengembalikan_200():
    response = client.get("/")
    assert response.status_code == 200
