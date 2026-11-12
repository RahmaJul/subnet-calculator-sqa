import pytest
from fastapi.testclient import TestClient

from main import app, hitung_subnet, alokasi_vlsm

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


# --- VLSM: Kasus Normal -----------------------------------------------------

def test_alokasi_vlsm_normal_kasus1():
    result = alokasi_vlsm("192.168.1.0/24", [100, 50, 20, 2])
    assert [item["kebutuhan"] for item in result] == [100, 50, 20, 2]
    assert [item["network_cidr"] for item in result] == [
        "192.168.1.0/25",
        "192.168.1.128/26",
        "192.168.1.192/27",
        "192.168.1.224/30",
    ]
    assert [item["usable_hosts"] for item in result] == [126, 62, 30, 2]
    for item in result:
        for key in ("kebutuhan", "network_cidr", "mask", "network", "broadcast", "first_host", "last_host", "usable_hosts"):
            assert key in item


def test_alokasi_vlsm_normal_kasus2():
    result = alokasi_vlsm("10.0.0.0/24", [60, 28, 12])
    assert [item["kebutuhan"] for item in result] == [60, 28, 12]
    assert [item["network_cidr"] for item in result] == [
        "10.0.0.0/26",
        "10.0.0.64/27",
        "10.0.0.96/28",
    ]
    assert [item["usable_hosts"] for item in result] == [62, 30, 14]
    for item in result:
        for key in ("kebutuhan", "network_cidr", "mask", "network", "broadcast", "first_host", "last_host", "usable_hosts"):
            assert key in item


# --- VLSM: Kasus Input Tidak Valid ------------------------------------------

@pytest.mark.parametrize(
    "network, kebutuhan",
    [
        ("192.168.1.0/24", [200, 100]),
        ("192.168.1.1/24", [10]),
        ("192.168.1.0/24", []),
        ("192.168.1.0/24", [0]),
    ],
)
def test_alokasi_vlsm_invalid(network, kebutuhan):
    with pytest.raises(ValueError):
        alokasi_vlsm(network, kebutuhan)


# --- API: POST /api/vlsm (Sukses) -------------------------------------------

def test_api_vlsm_sukses():
    response = client.post(
        "/api/vlsm",
        json={"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert [item["network_cidr"] for item in body] == [
        "192.168.1.0/25",
        "192.168.1.128/26",
        "192.168.1.192/27",
        "192.168.1.224/30",
    ]


# --- API: POST /api/vlsm (Input Tidak Valid) --------------------------------

@pytest.mark.parametrize(
    "network, kebutuhan",
    [
        ("192.168.1.0/24", [200, 100]),
        ("192.168.1.1/24", [10]),
        ("192.168.1.0/24", []),
        ("192.168.1.0/24", [0]),
    ],
)
def test_api_vlsm_invalid(network, kebutuhan):
    response = client.post(
        "/api/vlsm",
        json={"network": network, "kebutuhan_host": kebutuhan},
    )
    assert response.status_code == 400
    assert "detail" in response.json()

