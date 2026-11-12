# Kalkulator Subnet & VLSM

Aplikasi web kalkulator subnetting IPv4 dan VLSM berbasis FastAPI. Target pengguna: guru SMK TKJ.

## Menjalankan Lokal

```bash
uv sync --dev
uv run fastapi dev main.py
```

Buka http://127.0.0.1:8000

## Menjalankan Test

```bash
uv run pytest test_main.py -v --cov=main --cov-report=term-missing
```

## Docker

### Build image

```bash
docker build -t subnet-calculator .
```

### Jalankan container

```bash
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

Buka http://127.0.0.1:8000

### Smoke test ke container lokal

```bash
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```

Keluar kode 0 bila semua pemeriksaan lulus.

### Hentikan dan hapus container

```bash
docker rm -f subnet-app
```

## Deploy

Aplikasi dideploy di Vercel:

- URL Produksi: https://subnet-calculator-sqa-ten.vercel.app

### Smoke test ke URL produksi

```bash
uv run python scripts/smoke_test.py https://subnet-calculator-sqa-ten.vercel.app
```
