from dbfread import DBF
import pandas as pd

def esegui(df):
    def mappa_tipo(colonna,nome_colonna):
        dtype = colonna.dtype
        if  pd.api.types.is_string_dtype(colonna):
            max_len = max(colonna.astype(str).str.len().max(),1)
            min_len = min(int(max_len), 254)
            return f"{nome_colonna} C({min_len})"
        elif pd.api.types.is_integer_dtype(colonna):
            return f"{nome_colonna} N(10,0)"
        elif pd.api.types.is_float_dtype(colonna):
            return f"{nome_colonna} N(18,4)"
        elif object or pd.api.types.is_datetime64_any_dtype(colonna):
            return f"{nome_colonna} D"
        elif pd.api.types.is_bool_dtype(colonna):
            return f"{nome_colonna} L"
        else:
            return f"{nome_colonna} C(100)"
        
    print(df.dtypes)
    
    specifiche_campi = [mappa_tipo(df[col], str(col)[:10]) for col in df.columns]
    definizione_tabella = '; '.join(specifiche_campi)
    return definizione_tabella