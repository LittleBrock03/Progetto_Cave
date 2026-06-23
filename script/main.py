import argparse
import calendar
import os
import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd

import df_compress as dc
import df_format
import df_to_excel
import report_config

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"
ESEMPI_DIR = BASE_DIR / "esempi"
RETE_DIR = Path(r"\\172.16.2.13\arca\ditte\ICR")


def base_dbf_dir(sorgente):
    return RETE_DIR if sorgente == "rete" else ESEMPI_DIR


def verifica_percorsi(sorgente, dataset_config):
    base_dir = base_dbf_dir(sorgente)
    dbf_files = {
        source_config["file"]
        for source_config in dataset_config.get("sources", {}).values()
    }
    mancanti = [
        str(base_dir / file_name)
        for file_name in sorted(dbf_files)
        if not (base_dir / file_name).exists()
    ]
    config_da_verificare = [CONFIG_DIR / "report_config.json"]
    if "Cava" in set(dataset_config.get("calculated_fields", [])):
        config_da_verificare.append(CONFIG_DIR / "config_cava.txt")

    config_mancanti = [
        str(percorso)
        for percorso in config_da_verificare
        if not percorso.exists()
    ]

    if mancanti:
        raise FileNotFoundError("DBF mancanti:\n" + "\n".join(mancanti))
    if config_mancanti:
        raise FileNotFoundError("Config mancanti:\n" + "\n".join(config_mancanti))

    print(f"Sorgente DBF: {base_dir}")
    print(f"Config progetto: {CONFIG_DIR}")


def valida_data(stringa_input):
    try:
        return datetime.strptime(stringa_input, "%Y-%m").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Formato non valido. Usa YYYY-MM.") from exc


def mese_con_offset(data_riferimento, offset_mesi):
    mese_zero_based = data_riferimento.year * 12 + data_riferimento.month - 1 + offset_mesi
    anno = mese_zero_based // 12
    mese = mese_zero_based % 12 + 1
    return date(anno, mese, 1)


def periodo_mese(data_riferimento):
    anno = data_riferimento.year
    mese = data_riferimento.month
    menno = data_riferimento.strftime("%m/%Y")
    ultimo_giorno = calendar.monthrange(anno, mese)[1]

    data_inizio = data_riferimento.replace(day=1)
    data_fine = data_riferimento.replace(day=ultimo_giorno)
    print(f"Mese elaborato: {menno}")
    print(f"Data inizio:     {data_inizio}")
    print(f"Data fine:       {data_fine}")

    return menno, data_inizio, data_fine


def periodi_da_elaborare(numero_mesi=3, oggi=None):
    oggi = oggi or date.today()
    return [
        periodo_mese(mese_con_offset(oggi, -offset))
        for offset in range(numero_mesi)
    ]


def carica_cave(percorso):
    mappa = {}
    with open(percorso, "r", encoding="utf-8") as f:
        next(f)
        for riga in f:
            riga = riga.strip()
            if not riga:
                continue
            prefisso, cava = riga.split()
            mappa[prefisso] = cava
    return mappa


def _applica_colonne_dataset(df, dataset_config):
    keep_columns = dataset_config.get("keep_columns", [])
    if keep_columns:
        colonne = [col for col in keep_columns if col in df.columns]
        df = df[colonne]

    rename_columns = dataset_config.get("rename_columns", {})
    if rename_columns:
        df = df.rename(columns=rename_columns)

    return df


def _calcola_younth(df, menno):
    df = df.rename(columns={"data_documento": "Younth"})
    if menno[0] == "__RANGE__":
        df["Younth"] = pd.to_datetime(df["Younth"], errors="coerce").dt.strftime("%m/%Y")
    else:
        df["Younth"] = menno[0]
    return df


def _calcola_cava(df):
    mappa_cave = carica_cave(CONFIG_DIR / "config_cava.txt")
    df["Cava"] = (
        df["Codice_Articolo"]
        .astype(str)
        .str[:2]
        .map(mappa_cave)
        .fillna("CAVA_NON_MAPPATA")
    )
    return df


def _calcola_val_tot(df):
    df["Sconti_Docrig"] = (
        df["Sconti_Docrig"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace("EUR", "", regex=False)
        .str.strip()
    )
    df["Sconti_Docrig"] = pd.to_numeric(df["Sconti_Docrig"], errors="coerce").fillna(0)

    df["Val_tot"] = (
        (
            df["prezzo_unitario_docrig"]
            - (df["prezzo_unitario_docrig"] * df["Sconti_Docrig"] / 100)
            - df["sconti_valore_docrig"]
            + df["Prezzo_Trasp"]
        )
        * df["Quantita"]
    )
    return df


def applica_campi_calcolati(df, dataset_config, menno):
    calculated_fields = set(dataset_config.get("calculated_fields", []))

    if "Younth" in calculated_fields:
        df = _calcola_younth(df, menno)
    if "Cava" in calculated_fields:
        df = _calcola_cava(df)
    if "Val_tot" in calculated_fields:
        df = _calcola_val_tot(df)

    return df


def _condizione_report(df, regola):
    colonna = regola.get("column")
    operatore = regola.get("operator", "eq")
    if colonna not in df.columns:
        return pd.Series(False, index=df.index)

    serie = df[colonna]
    if operatore == "blank":
        testo = serie.astype("string").str.strip()
        return serie.isna() | testo.isin(["", "<NA>", "nan", "NaN", "None"])

    if operatore == "not_blank":
        testo = serie.astype("string").str.strip()
        return ~(serie.isna() | testo.isin(["", "<NA>", "nan", "NaN", "None"]))

    valore = regola.get("value")
    if isinstance(valore, (int, float)):
        numeri = pd.to_numeric(serie, errors="coerce")
        if operatore == "eq":
            return numeri.eq(valore)
        if operatore == "ne":
            return numeri.ne(valore)

    testo = serie.astype("string").str.strip()
    valore_testo = str(valore).strip()
    if operatore == "eq":
        return testo.eq(valore_testo)
    if operatore == "ne":
        return testo.ne(valore_testo)

    raise ValueError(f"Operatore filtro report non supportato: {operatore}")


def applica_filtri_report(df, config_report):
    df_filtrato = df
    for filtro in config_report.get("drop_rows", []):
        condizioni = filtro.get("all", [])
        if not condizioni:
            continue

        maschera = pd.Series(True, index=df_filtrato.index)
        for regola in condizioni:
            maschera &= _condizione_report(df_filtrato, regola)

        df_filtrato = df_filtrato.loc[~maschera].copy()

    return df_filtrato


def prepara_base_dati(menno, sorgente, dataset_config):
    df = df_format.esegui(base_dbf_dir(sorgente), dataset_config, menno)
    df = _applica_colonne_dataset(df, dataset_config)
    df = applica_campi_calcolati(df, dataset_config, menno)
    return df


def applica_config_report(df, config_report):
    df = applica_filtri_report(df, config_report)
    group_by = config_report.get("group_by", [])
    aggregazioni = config_report.get("aggregations")
    df_report = dc.esegui(df, group_by, aggregazioni)

    colonne = config_report.get("columns")
    if colonne:
        colonne_presenti = [col for col in colonne if col in df_report.columns]
        df_report = df_report[colonne_presenti]

    ordinamento = config_report.get("sort_by", group_by)
    if ordinamento:
        colonne_ordinamento = [col for col in ordinamento if col in df_report.columns]
        if colonne_ordinamento:
            df_report = df_report.sort_values(colonne_ordinamento, kind="stable")

    return df_report


def prepara_config_periodo(config_report, menno):
    config_periodo = config_report.copy()
    config_periodo["periodo"] = menno[0]
    config_periodo["periodo_file"] = menno[1].strftime("%Y-%m")
    return config_periodo


def periodo_intervallo(periodi):
    data_inizio = min(periodo[1] for periodo in periodi)
    data_fine = max(periodo[2] for periodo in periodi)
    print(f"Intervallo lettura DBF: {data_inizio} -> {data_fine}")
    return "__RANGE__", data_inizio, data_fine


def esegui_periodo(menno, nome_report=None, sorgente="rete"):
    config_report = report_config.carica(CONFIG_DIR / "report_config.json", nome_report)
    config_report = prepara_config_periodo(config_report, menno)
    df_base = prepara_base_dati(menno, sorgente, config_report["dataset_config"])
    df_report = applica_config_report(df_base, config_report)
    return df_report, config_report


def esegui_tutto(nome_report=None, sorgente="rete", numero_mesi=3):
    risultati = []
    periodi = periodi_da_elaborare(numero_mesi)
    if not periodi:
        return risultati

    config_report_base = report_config.carica(CONFIG_DIR / "report_config.json", nome_report)
    dataset_config = config_report_base["dataset_config"]
    df_base = prepara_base_dati(periodo_intervallo(periodi), sorgente, dataset_config)

    for menno in periodi:
        config_report = prepara_config_periodo(config_report_base, menno)
        df_periodo = df_base[df_base["Younth"].eq(menno[0])].copy()
        df_report = applica_config_report(df_periodo, config_report)
        risultati.append((df_report, config_report))
    return risultati


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Genera report Excel dai DBF.")
        parser.add_argument("--report", help="Nome report definito in config/report_config.json")
        parser.add_argument(
            "--source",
            choices=["rete", "esempi"],
            default="rete",
            help="Sorgente DBF. In produzione usa rete: i DBF sono nella cartella ICR; i config restano nel progetto.",
        )
        parser.add_argument(
            "--months",
            type=int,
            default=3,
            help="Numero di mesi da generare, includendo il mese corrente.",
        )
        parser.add_argument(
            "--no-open",
            action="store_true",
            help="Non apre Excel al termine. Utile per esecuzione pianificata.",
        )
        args = parser.parse_args()

        config_verifica = report_config.carica(CONFIG_DIR / "report_config.json", args.report)
        verifica_percorsi(args.source, config_verifica["dataset_config"])

        percorsi_creati = []
        for df, config_report in esegui_tutto(args.report, args.source, args.months):
            print("Esportazione del file Excel in corso...")
            percorso = df_to_excel.esegui(df, config_report)
            percorsi_creati.append(percorso)

        if percorsi_creati and not args.no_open:
            os.startfile(percorsi_creati[0])
    except Exception as exc:
        print(f"ERRORE: {exc}")
        raise SystemExit(1)
