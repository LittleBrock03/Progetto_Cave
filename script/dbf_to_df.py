from datetime import date
from pathlib import Path
import struct

import pandas as pd


def _leggi_campi_dbf(f):
    f.seek(4)
    num_records = struct.unpack("<I", f.read(4))[0]
    header_len = struct.unpack("<H", f.read(2))[0]
    record_len = struct.unpack("<H", f.read(2))[0]
    f.seek(32)

    campi = {}
    while True:
        raw = f.read(32)
        if not raw or raw[0] == 0x0D:
            break

        nome = raw[:11].split(b"\x00", 1)[0].decode("ascii").strip()
        campi[nome] = {
            "tipo": chr(raw[11]),
            "lunghezza": raw[16],
            "decimali": raw[17],
        }

    offset = 1
    for campo in campi.values():
        campo["offset"] = offset
        offset += campo["lunghezza"]

    return num_records, header_len, record_len, campi


def _parse_valore(raw, tipo, decimali):
    if tipo == "C":
        return raw.decode("cp1252", errors="replace").strip()

    if tipo == "I":
        if raw in {b"\x00\x00\x00\x00", b"    "}:
            return None
        return struct.unpack("<i", raw[:4])[0]

    if tipo == "B":
        if raw == b"\x00" * len(raw):
            return 0.0
        return struct.unpack("<d", raw[:8])[0]

    if tipo == "Y":
        if raw == b"\x00" * len(raw):
            return 0.0
        return struct.unpack("<q", raw[:8])[0] / 10000

    raw = raw.strip()
    if not raw:
        return None

    if tipo == "D":
        testo = raw.decode("ascii", errors="ignore")
        if len(testo) != 8:
            return None
        return date(int(testo[:4]), int(testo[4:6]), int(testo[6:8]))

    if tipo in {"N", "F"}:
        testo = raw.decode("ascii", errors="ignore").strip()
        if not testo:
            return None
        try:
            return float(testo) if decimali else int(float(testo))
        except ValueError:
            return None

    if tipo == "L":
        return raw[:1].upper() in {b"T", b"Y"}

    return raw.decode("cp1252", errors="replace").strip()


def _leggi_record(record, nomi_campi, campi):
    valori = {}
    for nome in nomi_campi:
        campo = campi.get(nome)
        if campo is None:
            continue

        start = campo["offset"]
        end = start + campo["lunghezza"]
        valori[nome] = _parse_valore(
            record[start:end],
            campo["tipo"],
            campo["decimali"],
        )

    return valori


def esegui(percorso_dbf, col_u, msg, filtro=None):
    records = []

    with Path(percorso_dbf).open("rb") as f:
        num_records, header_len, record_len, campi = _leggi_campi_dbf(f)
        nomi_campi = [col for col in col_u if col in campi]
        f.seek(header_len)

        for _ in range(num_records):
            record_raw = f.read(record_len)
            if not record_raw:
                break
            if record_raw[:1] == b"*":
                continue

            record = _leggi_record(record_raw, nomi_campi, campi)
            if filtro is not None and not filtro(record):
                continue

            records.append({
                f"{col}_{msg}": record[col]
                for col in nomi_campi
            })

    colonne_output = [f"{col}_{msg}" for col in nomi_campi]
    return pd.DataFrame.from_records(records, columns=colonne_output)
