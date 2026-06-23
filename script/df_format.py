import pandas as pd
import dbf_to_df


def _colonna_con_suffix(colonna, suffix):
    return f"{colonna}_{suffix}"


def _leggi_sorgente(nome, source_config, base_dir, menno, dataframes):
    columns = source_config.get("columns", [])
    suffix = source_config.get("suffix", "")
    percorso = base_dir / source_config["file"]

    filtro_data = source_config.get("date_filter")
    filtro_in = source_config.get("filter_in")

    def filtro(record):
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
        filtro=filtro if filtro_data or filtro_in else None,
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
        df = pd.merge(
            df,
            dataframes[source_name]["df"],
            left_on=join_config["left_on"],
            right_on=join_config["right_on"],
            how=join_config.get("how", "left"),
        )

    return df
