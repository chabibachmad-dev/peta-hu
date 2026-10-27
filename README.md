# peta-hu

Peta offline mapsforge (`.map`) per wilayah Indonesia untuk **Launcher HU** (head unit Android).

## Isi rilis

Setiap rilis `peta-YYYY-MM` berisi:

| File | Wilayah |
|---|---|
| `nusa-tenggara.map` | Bali & Nusa Tenggara |
| `java.map` | Jawa |
| `sumatra.map` | Sumatra |
| `kalimantan.map` | Kalimantan |
| `sulawesi.map` | Sulawesi |
| `maluku.map` | Maluku |
| `papua.map` | Papua |
| `katalog.json` | Daftar wilayah untuk launcher |

"Seluruh Indonesia" tercantum di katalog tetapi diunduh langsung dari
[download.mapsforge.org](https://download.mapsforge.org/maps/v5/asia/indonesia.map).

Launcher membaca katalog dari
`https://github.com/chabibachmad-dev/peta-hu/releases/latest/download/katalog.json`.

## Format katalog

```json
{
  "versi": "2026-10",
  "wilayah": [
    {
      "id": "maluku",
      "nama": "Maluku",
      "cakupan": "Maluku & Maluku Utara",
      "url": "https://github.com/chabibachmad-dev/peta-hu/releases/download/peta-2026-10/maluku.map",
      "ukuran_byte": 28897323,
      "sha256": "…",
      "bbox": [-9.52, 123.89, 3.73, 135.41],
      "versi": "2026-10"
    }
  ]
}
```

`bbox` = `[minLat, minLon, maxLat, maxLon]` dari header file `.map`.

## Cara membuat

1. Unduh ekstrak `.osm.pbf` dari [Geofabrik](https://download.geofabrik.de/asia/indonesia.html).
2. Konversi dengan osmosis 0.49.2 + mapsforge-map-writer 0.25.0:
   `osmosis --rbf file=<wilayah>-latest.osm.pbf --mapfile-writer file=<wilayah>.map type=hd`
3. Jalankan `python katalog.py peta-YYYY-MM` untuk membuat `katalog.json` (bbox + sha256).

## Lisensi

Data peta © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), tersedia di bawah
[Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/).
