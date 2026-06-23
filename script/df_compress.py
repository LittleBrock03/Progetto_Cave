def esegui(df, group_by, aggregazioni=None):
    if not group_by:
        return df.copy()

    funzioni_aggregazione = aggregazioni or {
        "Descrizione_Riga": "first",
        "Quantita": "sum",
        "Val_tot": "sum",
        "Cava": "first",
        "Ragione_Sociale": "first",
    }

    df_compresso = (
        df.groupby(group_by, as_index=False)
        .agg(funzioni_aggregazione)
    )

    return df_compresso
