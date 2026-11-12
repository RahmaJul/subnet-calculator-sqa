# SPEC.md — Kalkulator Subnet & VLSM

## Tujuan

Dokumen ini mendefinisikan perilaku, kontrak fungsi, kontrak API, tampilan UI,
dan kasus uji untuk Kalkulator Subnet & VLSM berbasis web. Target pengguna
adalah guru SMK TKJ yang membutuhkan alat bantu verifikasi hasil subnetting
IPv4 secara cepat dan akurat. Kebenaran hasil harus dapat dinilai guru tanpa
membaca kode. Dokumen ini menjadi _single source of truth_ untuk pengembang,
penguji, dan reviewer.

---

## Aturan Validasi

### Alamat IP
- Tepat 4 oktet, dipisahkan titik.
- Tiap oktet adalah bilangan bulat 0–255.
- Tidak boleh ada angka nol di depan: `192.168.01.1` ditolak, `192.168.1.1` diterima.
- Tidak boleh ada spasi (termasuk trailing/leading space).
- Format lain (teks, kosong, kurang/lebih dari 4 oktet) ditolak.

### Prefix
- Bilangan bulat 0–32.
- Prefix di luar rentang (misal 33, -1) ditolak.
- Bukan bilangan bulat (misal `24.5`, teks) ditolak.

### Perilaku saat tidak valid
- Fungsi Python: `raise ValueError` dengan pesan yang jelas.
- Endpoint API: HTTP 400 dengan body JSON `{"detail": "<pesan error>"}`.

---

## Kontrak Fungsi

### `hitung_subnet(ip: str, prefix: int) -> dict`

Mengembalikan dictionary dengan kunci:

| Kunci          | Tipe | Keterangan                                        |
| -------------- | ---- | ------------------------------------------------- |
| `mask`         | str  | Subnet mask desimal bertitik, misal `255.255.255.128` |
| `network`      | str  | Network address (bitwise AND antara IP dan mask)  |
| `broadcast`    | str  | Broadcast address; `None` untuk /31 dan /32       |
| `first_host`   | str  | Host pertama yang dapat dipakai                   |
| `last_host`    | str  | Host terakhir yang dapat dipakai                  |
| `usable_hosts` | int  | Jumlah host yang dapat dipakai                    |

**Aturan khusus:**

- Prefix 0–30: `usable_hosts = 2^(32-prefix) - 2`; broadcast dihitung dari
  bitwise OR antara network dan inverse mask.
- Prefix /31 (RFC 3021, point-to-point): `usable_hosts = 2`, `broadcast = None`,
  `first_host` dan `last_host` adalah dua IP di blok tersebut.
- Prefix /32 (host route): `usable_hosts = 1`, `broadcast = None`,
  `first_host = last_host = ip`.
- Network address dihitung dengan operasi **bitwise AND** antara representasi
  integer IP dan subnet mask.

---

### `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`

Mengalokasikan blok subnet dari satu network besar untuk daftar kebutuhan host.

**Langkah algoritma:**
1. Validasi `network_cidr` adalah alamat jaringan yang valid (bukan host address).
2. Urutkan `kebutuhan_host` dari terbesar ke terkecil.
3. Untuk tiap kebutuhan, hitung ukuran blok: pangkat 2 terkecil yang ≥
   kebutuhan + 2 (minimal /30 → 4 alamat).
4. Alokasikan blok berurutan mulai dari alamat network.
5. Tiap hasil memuat: `kebutuhan`, `network_cidr`, dan semua kunci `hitung_subnet`.

**Raise `ValueError` bila:**
- `network_cidr` bukan alamat jaringan yang valid (host bit aktif).
- Daftar `kebutuhan_host` kosong atau berisi nilai < 1.
- Total ruang alamat tidak cukup menampung seluruh kebutuhan.

---

## Kontrak API

### `GET /`
- Mengembalikan `index.html`.
- Status: `200 OK`.

### `GET /api/subnet?ip=<ip>&prefix=<prefix>`
- Memanggil `hitung_subnet(ip, prefix)`.
- Sukses: `200 OK` + JSON semua kunci kontrak fungsi.
- Input tidak valid: `400 Bad Request` + `{"detail": "<pesan>"}`.

**Contoh respons sukses:**
```json
{
  "mask": "255.255.255.128",
  "network": "172.16.5.128",
  "broadcast": "172.16.5.255",
  "first_host": "172.16.5.129",
  "last_host": "172.16.5.254",
  "usable_hosts": 126
}
```

### `POST /api/vlsm`
- Body JSON: `{"network": "<cidr>", "kebutuhan_host": [<int>, ...]}`.
- Memanggil `alokasi_vlsm(network, kebutuhan_host)`.
- Sukses: `200 OK` + JSON array, tiap elemen memuat `kebutuhan`, `network_cidr`,
  dan semua kunci `hitung_subnet`.
- Input tidak valid atau tidak muat: `400 Bad Request` + `{"detail": "<pesan>"}`.

**Semua error dikembalikan sebagai `{"detail": "..."}` — bukan HTML, bukan stack trace.**

---

## Halaman Web

Satu halaman HTML (`index.html`) dengan dua tab: **Subnet** dan **VLSM**.
Gaya visual: bersih, minimalis, light mode — putih, abu-abu lunak, aksen biru,
sudut membulat (seperti jodies.id / Google Calculator).

### Tab Subnet
- Input: field alamat IP + field prefix (0–32) + tombol **Hitung**.
- Hasil: kartu berisi mask, network, broadcast, first host, last host,
  usable hosts.
- Error: pesan merah jelas di bawah field (dari field `detail`).

### Tab VLSM
- Input: field network dalam notasi CIDR + daftar kebutuhan host
  (bisa ditambah/hapus baris).
- Hasil: tabel berisi urutan alokasi, kebutuhan, network CIDR, range host,
  jumlah host.
- Error: pesan merah jelas bila validasi gagal.

### Tiga state yang harus ditangani
1. **Kosong** — form bersih, belum ada hasil.
2. **Sukses** — kartu/tabel hasil tampil, tidak ada pesan error.
3. **Error** — pesan dari `detail` tampil, tidak ada kartu/tabel hasil.

### Koneksi ke API
- Tab Subnet: `GET /api/subnet?ip=...&prefix=...`
- Tab VLSM: `POST /api/vlsm` dengan body JSON.
- Semua komunikasi pakai `fetch` JavaScript, tanpa reload halaman.
- Error HTTP 400 ditampilkan ke pengguna dari field `detail`.

---

## Tabel Test Case

### Subnet — Kasus Normal

| Input IP      | Prefix | network       | broadcast       | first_host    | last_host       | usable_hosts |
| ------------- | ------ | ------------- | --------------- | ------------- | --------------- | ------------ |
| 172.16.5.130  | 25     | 172.16.5.128  | 172.16.5.255    | 172.16.5.129  | 172.16.5.254    | 126          |
| 10.0.0.0      | 30     | 10.0.0.0      | 10.0.0.3        | 10.0.0.1      | 10.0.0.2        | 2            |
| 192.168.1.1   | 24     | 192.168.1.0   | 192.168.1.255   | 192.168.1.1   | 192.168.1.254   | 254          |
| 10.0.0.0      | 8      | 10.0.0.0      | 10.255.255.255  | 10.0.0.1      | 10.255.255.254  | 16777214     |

### Subnet — Edge Case

| Input IP      | Prefix | network       | broadcast | first_host    | last_host     | usable_hosts | Catatan                   |
| ------------- | ------ | ------------- | --------- | ------------- | ------------- | ------------ | ------------------------- |
| 192.168.1.0   | 31     | 192.168.1.0   | None      | 192.168.1.0   | 192.168.1.1   | 2            | RFC 3021 point-to-point   |
| 192.168.1.5   | 32     | 192.168.1.5   | None      | 192.168.1.5   | 192.168.1.5   | 1            | Host route                |
| 0.0.0.0       | 0      | 0.0.0.0       | 255.255.255.255 | 0.0.0.1  | 255.255.255.254 | 4294967294   | Default route             |

### Subnet — Input Tidak Valid (harus raise ValueError / HTTP 400)

| Input IP         | Prefix | Alasan Ditolak                  |
| ---------------- | ------ | ------------------------------- |
| 256.1.1.1        | 24     | Oktet pertama > 255             |
| 192.168.01.1     | 24     | Angka nol di depan              |
| 192.168.1        | 24     | Kurang dari 4 oktet             |
| abc              | 24     | Bukan angka                     |
| (kosong)         | 24     | Input kosong                    |
| 192.168.1.1      | 33     | Prefix > 32                     |
| 192.168.1.1      | -1     | Prefix negatif                  |
| "192.168.1.1 "   | 24     | Ada spasi (trailing space)      |

### VLSM — Kasus Normal

| Network          | Kebutuhan Host   | Hasil Alokasi (urut terbesar ke terkecil)                                                                                           |
| ---------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 192.168.1.0/24   | [100, 50, 20, 2] | 192.168.1.0/25 (126 host), 192.168.1.128/26 (62 host), 192.168.1.192/27 (30 host), 192.168.1.224/30 (2 host) |
| 10.0.0.0/24      | [60, 28, 12]     | 10.0.0.0/26 (62 host), 10.0.0.64/27 (30 host), 10.0.0.96/28 (14 host)                                        |

### VLSM — Input Tidak Valid (harus raise ValueError / HTTP 400)

| Input                              | Alasan Ditolak                                        |
| ---------------------------------- | ----------------------------------------------------- |
| 192.168.1.0/24, kebutuhan [200, 100] | Tidak muat: total blok melebihi ruang /24           |
| 192.168.1.1/24, kebutuhan [10]     | network_cidr bukan alamat jaringan (host bit aktif)   |
| 192.168.1.0/24, kebutuhan []       | Daftar kebutuhan kosong                               |
| 192.168.1.0/24, kebutuhan [0]      | Nilai kebutuhan < 1                                   |

---

## Di Luar Cakupan

Fitur berikut tidak termasuk dalam versi ini:

- Dukungan IPv6.
- Supernetting / route summarization.
- Autentikasi atau manajemen pengguna.
- Penyimpanan riwayat perhitungan.
- Export hasil ke PDF atau CSV.
- Dark mode.
- Validasi format CIDR di luar konteks VLSM (tab subnet pakai field IP + prefix
  terpisah, bukan CIDR).
