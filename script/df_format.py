import pandas as pd
import dbf_to_df


def _colonna_con_suffix(colonna, suffix):
    return f"{colonna}_{suffix}"


def _valore_testo(serie):
    return serie.astype("string").fillna("").str.strip()


def _applica_trasformazione_chiave(df, transform_config):
    colonna = transform_config["column"]
    if colonna not in df.columns:
        raise KeyError(f"Colonna join non trovata: {colonna}")

    chiave = _valore_testo(df[colonna])

    if "left" in transform_config:
        chiave = chiave.str[:transform_config["left"]]
    if "right" in transform_config:
        chiave = chiave.str[-transform_config["right"]:]
    if "prefix" in transform_config:
        chiave = transform_config["prefix"] + chiave
    if "suffix" in transform_config:
        chiave = chiave + transform_config["suffix"]

    return chiave


def _testo_record(record, colonna):
    valore = record.get(colonna)
    return "" if valore is None else str(valore).strip()


def _condizione_record(record, regola):
    colonna = regola.get("column")
    operatore = regola.get("operator", "eq")
    testo = _testo_record(record, colonna)
    valore = str(regola.get("value", "")).strip()

    if operatore == "blank":
        return testo == ""
    if operatore == "not_blank":
        return testo != ""
    if operatore == "eq":
        return testo == valore
    if operatore == "ne":
        return testo != valore
    if operatore == "ge":
        return testo >= valore
    if operatore == "le":
        return testo <= valore
    if operatore == "gt":
        return testo > valore
    if operatore == "lt":
        return testo < valore
    if operatore == "between":
        return str(regola["min"]).strip() <= testo <= str(regola["max"]).strip()
    if operatore == "starts_with":
        return testo.startswith(valore)
    if operatore == "in":
        valori = {str(item).strip() for item in regola.get("values", [])}
        return testo in valori

    raise ValueError(f"Operatore filtro sorgente non supportato: {operatore}")


def _maschera_record(record, gruppo):
    if "all" in gruppo:
        return all(_maschera_record(record, regola) for regola in gruppo.get("all", []))
    if "any" in gruppo:
        return any(_maschera_record(record, regola) for regola in gruppo.get("any", []))
    return _condizione_record(record, gruppo)


def _prepara_chiave_join(df, join_config, lato):
    colonna_config = f"{lato}_on"
    transform_config = join_config.get(f"{lato}_transform")

    if not transform_config:
        return join_config[colonna_config], df

    nome_chiave = f"__join_{lato}_{id(join_config)}"
    df = df.copy()
    df[nome_chiave] = _applica_trasformazione_chiave(df, transform_config)
    return nome_chiave, df


def _leggi_sorgente(nome, source_config, base_dir, menno, dataframes):
    columns = source_config.get("columns", [])
    suffix = source_config.get("suffix", "")
    percorso = base_dir / source_config["file"]

    filtro_data = source_config.get("date_filter")
    filtro_in = source_config.get("filter_in")
    row_filter = source_config.get("row_filter")

    def filtro(record):
        if row_filter and not _maschera_record(record, row_filter):
            return False

        if filtro_data:
            valore = record.get(filtro_data["column"])
            if not (pd.Timestamp(menno[1]) <= pd.Timestamp(valore) <= pd.Timestamp(menno[2])):
                return False

        if filtro_in:
            source_name = filtro_in["source"]
            source_column = _colonna_con_suffix(
                filtro_in["source_column"],
                dataframes[source_name]["suffix"],
            )
            valori_validi = dataframes[source_name]["values"][source_column]
            if record.get(filtro_in["column"]) not in valori_validi:
                return False

        return True

    df = dbf_to_df.esegui(
        percorso,
        columns,
        suffix,
        filtro=filtro if filtro_data or filtro_in or row_filter else None,
    )

    value_sets = {
        colonna: set(df[colonna])
        for colonna in df.columns
    }

    return {
        "df": df,
        "suffix": suffix,
        "values": value_sets,
    }


def esegui(base_dir, dataset_config, menno):
    dataframes = {}
    sources = dataset_config.get("sources", {})

    for nome, source_config in sources.items():
        dataframes[nome] = _leggi_sorgente(nome, source_config, base_dir, menno, dataframes)

    base_source = dataset_config["base_source"]
    df = dataframes[base_source]["df"]

    for join_config in dataset_config.get("joins", []):
        source_name = join_config["source"]
        right_df = dataframes[source_name]["df"]
        left_on, df = _prepara_chiave_join(df, join_config, "left")
        right_on, right_df = _prepara_chiave_join(right_df, join_config, "right")

        df = pd.merge(
            df,
            right_df,
            left_on=left_on,
            right_on=right_on,
            how=join_config.get("how", "left"),
        )

        colonne_temporanee = [col for col in (left_on, right_on) if col.startswith("__join_")]
        if colonne_temporanee:
            df = df.drop(columns=[col for col in colonne_temporanee if col in df.columns])

    return df
