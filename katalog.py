"""Buat katalog.json untuk rilis peta-hu dari file *.map di folder ini.

Pakai: python katalog.py <tag-rilis>
bbox dibaca dari header mapsforge; sha256 disimpan di cache <nama>.map.sha256 (dihitung ulang bila ukuran/waktu berubah).
"""
import hashlib
import json
import os
import struct
import sys

REPO = "chabibachmad-dev/peta-hu"
VERSI = "2026-10"

WILAYAH = [
    ("nusa-tenggara", "Bali & Nusa Tenggara", "Bali, Lombok, Sumbawa, Flores, Sumba, Timor"),
    ("java", "Jawa", "Jawa, Madura, Jakarta, Banten, Yogyakarta"),
    ("sumatra", "Sumatra", "Sumatra, Riau, Kepulauan Riau, Bangka Belitung"),
    ("kalimantan", "Kalimantan", "Kalimantan Barat, Tengah, Selatan, Timur, Utara"),
    ("sulawesi", "Sulawesi", "Sulawesi Utara, Tengah, Selatan, Tenggara, Barat, Gorontalo"),
    ("maluku", "Maluku", "Maluku & Maluku Utara"),
    ("papua", "Papua", "Papua & Papua Barat"),
]

INDONESIA = {
    "id": "indonesia",
    "nama": "Seluruh Indonesia",
    "cakupan": "Semua pulau (mapsforge.org, satu file besar)",
    "url": "https://download.mapsforge.org/maps/v5/asia/indonesia.map",
    "ukuran_byte": 1852193034,
    "sha256": "ce879e164ce1a5a71ac210e1aa86ceca23b52b49b2c65c712fe4f1f34384f194",
    "bbox": [-11.70655, 92.66481, 7.09933, 141.1217],
    "versi": "2026-09",
}


def bbox(path):
    with open(path, "rb") as f:
        head = f.read(64)
    if head[:20] != b"mapsforge binary OSM":
        raise ValueError(path + ": bukan file mapsforge")
    # magic(20) headerSize(4) version(4) fileSize(8) date(8) lalu bbox 4x int32 mikroderajat
    min_lat, min_lon, max_lat, max_lon = struct.unpack(">4i", head[44:60])
    return [round(v / 1e6, 6) for v in (min_lat, min_lon, max_lat, max_lon)]


def sha256(path):
    st = os.stat(path)
    cache = path + ".sha256"
    key = "%d %d" % (st.st_size, int(st.st_mtime))
    if os.path.exists(cache):
        k, h = open(cache).read().split("\n")[:2]
        if k == key:
            return h
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    open(cache, "w").write(key + "\n" + h.hexdigest() + "\n")
    return h.hexdigest()


def main():
    tag = sys.argv[1]
    here = os.path.dirname(os.path.abspath(__file__))
    out = []
    for wid, nama, cakupan in WILAYAH:
        path = os.path.join(here, wid + ".map")
        if not os.path.exists(path):
            print("lewati (belum ada):", wid)
            continue
        out.append({
            "id": wid,
            "nama": nama,
            "cakupan": cakupan,
            "url": "https://github.com/%s/releases/download/%s/%s.map" % (REPO, tag, wid),
            "ukuran_byte": os.path.getsize(path),
            "sha256": sha256(path),
            "bbox": bbox(path),
            "versi": VERSI,
        })
        print(wid, out[-1]["ukuran_byte"], out[-1]["bbox"])
    out.append(INDONESIA)
    katalog = {"versi": VERSI, "sumber": "OpenStreetMap contributors (ODbL), Geofabrik, mapsforge", "wilayah": out}
    with open(os.path.join(here, "katalog.json"), "w", encoding="utf-8") as f:
        json.dump(katalog, f, ensure_ascii=False, indent=2)
    print("katalog.json:", len(out), "wilayah")


if __name__ == "__main__":
    main()
