# [Feature] Kalkulator Subnet

## Deskripsi

Membangun aplikasi web (Single Page Application) dengan backend Python 3.12
(FastAPI) untuk menghitung parameter subnetting IPv4. Aplikasi ini menyediakan
dua fungsi inti yang diuji secara menyeluruh dengan `pytest`:

- `hitung_subnet(ip: str, prefix: int) -> dict` — menghitung parameter subnet
  (mask, network, broadcast, first_host, last_host, usable_hosts) berdasarkan
  IP dan prefix CIDR, termasuk *edge cases* RFC 3021 (`/31`) dan host route
  (`/32`).
- Endpoint API `GET /`, `GET /api/subnet`, dan `POST /api/vlsm` untuk
  menyajikan UI HTML dan hasil kalkulasi subnet/VLSM dalam bentuk JSON.

Seluruh detail teknis (aturan validasi, kontrak fungsi, kontrak API, dan tabel
test case) mengacu pada `SPEC.md`.

## Tugas

- [ ] Implementasikan validasi input sesuai *Aturan Validasi* di `SPEC.md`
      (IPv4 tanpa *leading zeros*, prefix `0..32`, kebutuhan host `>= 1`).
- [ ] Implementasikan `hitung_subnet` pada `main.py` dengan logika bitwise
      dan penanganan khusus `/31` dan `/32`.
- [ ] Implementasikan `alokasi_vlsm` pada `main.py` dengan alokasi descending
      dan batas blok terkecil `/30`.
- [ ] Implementasikan endpoint `GET /`, `GET /api/subnet`, dan `POST /api/vlsm`.
- [ ] Sajikan antarmuka web (`index.html`) dengan tab Mode Subnet dan Mode VLSM.
- [ ] Tulis seluruh test case di `test_main.py` sesuai tabel test `SPEC.md`.

## Kriteria Penerimaan

Seluruh test case pada tabel berikut (merujuk `SPEC.md` §6) harus lulus dengan
`pytest`:

| Kasus | Input | Hasil yang Diharapkan | Status |
| --- | --- | --- | --- |
| Subnet Standar | `172.16.5.130/25` | Network: `172.16.5.128`, Broadcast: `172.16.5.255`, Host: 126 | Lulus |
| Blok Minimum Standar | `10.0.0.0/30` | Host `.1` sampai `.2`, Broadcast: `.3`, Host: 2 | Lulus |
| Point-to-Point (RFC 3021) | `192.168.1.0/31` | Point-to-point, Broadcast: `None`, Host: 2 | Lulus |
| Host Route | `192.168.1.5/32` | Network/IP/Broadcast tunggal, Host: 1 | Lulus |
| IP Tidak Valid (Oktet >255) | `256.1.1.1/24` | Ditolak (ValueError / HTTP 400) | Lulus |
| IP Tidak Valid (Leading Zero) | `192.168.01.1/24` | Ditolak (ValueError / HTTP 400) | Lulus |
| Format Input Rusak | `192.168.1`, `abc`, Kosong | Ditolak (ValueError / HTTP 400) | Lulus |
| Prefix di Luar Batas | Prefix `33`, Prefix `-1` | Ditolak (ValueError / HTTP 400) | Lulus |
| VLSM: Alokasi Normal | `192.168.1.0/24` (Host: 100, 50, 20, 2) | `/25` (.0), `/26` (.128), `/27` (.192), `/30` (.224) | Lulus |
| VLSM: Kapasitas Overload | `192.168.1.0/24` (Host: 200, 100) | Ditolak, blok tidak cukup (ValueError / HTTP 400) | Lulus |

## Alur Kerja

1. **Issue** — Issue dibuat di GitHub dari dokumen ini.
2. **Branch** — Buat branch `feature/issue-<nomor>-subnet-calculator` dari `main`.
3. **Test dulu** — Tulis test di `test_main.py` terlebih dahulu (TDD *red*).
4. **Implementasi** — Implementasikan `hitung_subnet`/`alokasi_vlsm` dan API
   hingga test *green*.
5. **Commit** — Commit perubahan dengan pesan yang deskriptif.
6. **Pull request** — Buka PR dari branch menuju `main`.
7. **CI** — Pastikan pipeline CI (test + coverage) lulus.
8. **Merge** — Merge PR ke `main` setelah review dan CI hijau.
