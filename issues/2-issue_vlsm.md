# [Feature] Kalkulator VLSM

## Deskripsi

Menambahkan fitur **Variable Length Subnet Masking (VLSM)** pada aplikasi
Kalkulator Subnet & VLSM berbasis web. Fitur ini memungkinkan guru SMK TKJ
mengalokasikan beberapa blok subnet dari satu network besar sesuai kebutuhan
host masing-masing departemen/ruangan secara efisien.

Fungsi inti yang diimplementasikan:

- `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`
  — mengalokasikan blok subnet secara berurutan dari address terbesar ke terkecil,
  menggunakan ukuran blok pangkat 2 terkecil yang memenuhi kebutuhan (minimal `/30`).
- Endpoint API `POST /api/vlsm` menerima body JSON `{"network": "<cidr>",
  "kebutuhan_host": [<int>, ...]}` dan mengembalikan array JSON hasil alokasi.

Seluruh detail teknis (algoritma alokasi, aturan validasi, dan tabel test case)
mengacu pada `SPEC.md` bagian *Kontrak Fungsi* dan *Tabel Test Case VLSM*.

## Tugas

- [ ] Implementasikan `alokasi_vlsm` pada `main.py` dengan algoritma:
      1. Validasi `network_cidr` adalah alamat jaringan yang valid (bukan host address).
      2. Urutkan `kebutuhan_host` dari terbesar ke terkecil.
      3. Hitung ukuran blok: pangkat 2 terkecil yang ≥ kebutuhan + 2 (minimal `/30` → 4 alamat).
      4. Alokasikan blok berurutan mulai dari alamat network.
      5. Tiap hasil memuat: `kebutuhan`, `network_cidr`, dan semua kunci `hitung_subnet`.
- [ ] Raise `ValueError` bila:
      - `network_cidr` bukan alamat jaringan yang valid (host bit aktif).
      - Daftar `kebutuhan_host` kosong atau berisi nilai < 1.
      - Total ruang alamat tidak cukup menampung seluruh kebutuhan.
- [ ] Implementasikan endpoint `POST /api/vlsm` di `main.py`.
- [ ] Hubungkan tab VLSM di `index.html` ke endpoint `/api/vlsm` (tampilkan
      hasil tabel dan pesan error dari field `detail`).
- [ ] Tulis seluruh test case VLSM di `test_main.py` sesuai tabel test `SPEC.md`.

## Kriteria Penerimaan

Seluruh test case VLSM pada tabel berikut (merujuk `SPEC.md` §Tabel Test Case)
harus lulus dengan `pytest`:

| Kasus | Input | Hasil yang Diharapkan | Status |
| --- | --- | --- | --- |
| Alokasi Normal 4 subnet | `192.168.1.0/24`, Host: `[100, 50, 20, 2]` | `/25` (.0, 126 host), `/26` (.128, 62 host), `/27` (.192, 30 host), `/30` (.224, 2 host) | Lulus |
| Alokasi Normal 3 subnet | `10.0.0.0/24`, Host: `[60, 28, 12]` | `/26` (.0, 62 host), `/27` (.64, 30 host), `/28` (.96, 14 host) | Lulus |
| Semua kunci hitung_subnet tersedia | Tiap elemen hasil | Memuat `mask`, `network`, `broadcast`, `first_host`, `last_host`, `usable_hosts` | Lulus |
| Kapasitas Overload | `192.168.1.0/24`, Host: `[200, 100]` | Ditolak — blok tidak cukup (ValueError / HTTP 400) | Lulus |
| Host bit aktif (bukan network) | `192.168.1.1/24`, Host: `[10]` | Ditolak — bukan alamat jaringan (ValueError / HTTP 400) | Lulus |
| Daftar kebutuhan kosong | `192.168.1.0/24`, Host: `[]` | Ditolak — daftar kosong (ValueError / HTTP 400) | Lulus |
| Nilai kebutuhan < 1 | `192.168.1.0/24`, Host: `[0]` | Ditolak — nilai kebutuhan < 1 (ValueError / HTTP 400) | Lulus |
| API sukses (`POST /api/vlsm`) | `192.168.1.0/24`, Host: `[100, 50, 20, 2]` | HTTP 200 + array network_cidr `/25`, `/26`, `/27`, `/30` | Lulus |
| API overload (`POST /api/vlsm`) | `192.168.1.0/24`, Host: `[200, 100]` | HTTP 400 + field `detail` | Lulus |

## Alur Kerja

1. **Issue** — Issue dibuat di GitHub dari dokumen ini.
2. **Branch** — Buat branch `feature/issue-<nomor>-vlsm` dari `main` terbaru.
3. **Test dulu** — Tambahkan test VLSM ke `test_main.py` (TDD *red*).
4. **Kerangka** — Tambahkan `alokasi_vlsm` stub (`raise NotImplementedError`)
   dan endpoint `POST /api/vlsm` ke `main.py`; pastikan test merah.
5. **Implementasi** — Implementasikan hingga semua test hijau.
6. **Commit** — Commit dengan pesan deskriptif.
7. **Pull request** — Buka PR dari branch menuju `main`.
8. **CI** — Pastikan pipeline CI (test + coverage) lulus.
9. **Merge** — Merge PR ke `main` setelah CI hijau.
