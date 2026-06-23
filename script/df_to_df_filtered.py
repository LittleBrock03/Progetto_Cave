from datetime import date
import validate_input
import pandas


def esegui(df):

    df = df.copy()
    # ---------------------
    # FUNZIONE FILTRO DATI
    # ---------------------
    def filter_datafield(df):

        tipo = validate_input.esegui("Inserisci il tipo di campo da cercare (C, N, D, L): ", 'str', opzione_aggiuntive=['C', 'N', 'D', 'L']).upper()
            
                
        def trova_tipo(df, tipo):

            for col in df.columns:
                print(f"Colonna: {col}, Tipo: {df[col].dtype}")
            return [col for col in df.columns for t in tipo if df[col].dtype == t]


        def chiedi_data(nome):
            print(f"\n Inserisci la data di {nome}:")
            anno = validate_input.esegui("Anno (YYYY): ", int, minimo=1900, massimo=date.today().year)
            mese = validate_input.esegui("Mese (MM): ", int, minimo=1, massimo=12)
            giorno = validate_input.esegui("Giorno (DD): ", int, minimo=1, massimo=31)
            return pandas.Timestamp(date(anno, mese, giorno))

        def switch_filter(tipo):

            if tipo == 'C':
                campi_testo = trova_tipo(df, {'str'})
                if not campi_testo:
                    print("Nessun campo di tipo testo trovato nella df.")
                    exit()
                
                elif len(campi_testo) == 1:
                    print(f"\n Campi di tipo testo trovati: {campi_testo}")
                    campo_testo = campi_testo[0]
                    filtro = validate_input.esegui(f"Inserisci il filtro per il campo {campo_testo}: ", 'str')   

                    df_filter = df[df[campo_testo].str.contains(filtro, case=False, na=False)]
                    return df_filter
                campo_testo = campi_testo[validate_input.esegui(f"\n Campi di tipo testo trovati: {campi_testo}\n Seleziona il numero del campo da filtrare (1-{len(campi_testo)}): ", int, minimo=1, massimo=len(campi_testo)) - 1]
                filtro = validate_input.esegui(f"Inserisci il filtro per il campo {campo_testo}: ", 'str')
                df_filter = df[df[campo_testo].str.contains(filtro, case=False, na=False)]
                return df_filter

            elif tipo == 'N':
                campi_numerici = trova_tipo(df, {'int64', 'float64'})
                if not campi_numerici:
                    print("Nessun campo di tipo numerico trovato nella df.")
                    exit()
                elif len(campi_numerici) == 1:
                    print(f"\n Campi di tipo numerico trovati: {campi_numerici}")
                    campo_numerico = campi_numerici[0]
                    valore_min = validate_input.esegui(f"Inserisci il valore minimo per il campo {campo_numerico}: ", float, minimo=0)
                    valore_max = validate_input.esegui(f"Inserisci il valore massimo per il campo {campo_numerico}: ", float, minimo=valore_min)

                    df_filter = df[(df[campo_numerico] >= valore_min) & (df[campo_numerico] <= valore_max)]
                    return df_filter
                campo_numerico = campi_numerici[validate_input.esegui(f"\n Campi di tipo numerico trovati: {campi_numerici}\n Seleziona il numero del campo da filtrare (1-{len(campi_numerici)}): ", int, minimo=1, massimo=len(campi_numerici)) - 1]
                valore_min = validate_input.esegui(f"Inserisci il valore minimo per il campo {campo_numerico}: ", float, minimo=0)
                valore_max = validate_input.esegui(f"Inserisci il valore massimo per il campo {campo_numerico}: ", float, minimo=valore_min)
                df_filter = df[(df[campo_numerico] >= valore_min) & (df[campo_numerico] <= valore_max)]
                return df_filter
            
            elif tipo == 'L':
                campi_logici = trova_tipo(df, {'bool'})
                if not campi_logici:
                    print("Nessun campo di tipo logico trovato nella df.")
                    exit()
                elif len(campi_logici) == 1:
                    print(f"\n Campi di tipo logico trovati: {campi_logici}")
                    campo_logico = campi_logici[0]
                    valore_logico = validate_input.esegui(f"Inserisci il valore per il campo {campo_logico} (Vero/Falso): ", bool)
  
                    df_filter = df[df[campo_logico] == valore_logico]
                    return df_filter
                    # df_filter = df[(df[campo_numerico] >= valore_min) & (df[campo_numerico] <= valore_max)]
                    # return df_filter
                campo_logico = campi_logici[validate_input.esegui(f"\n Campi di tipo logico trovati: {campi_logici}\n Seleziona il numero del campo da filtrare (1-{len(campi_logici)}): ", int, minimo=1, massimo=len(campi_logici)) - 1]
                valore_logico = validate_input.esegui(f"Inserisci il valore per il campo {campo_logico} (Vero/Falso): ", bool)
                df_filter = df[df[campo_logico] == valore_logico]
                return df_filter
            
            elif tipo == 'D':
                campi_data = trova_tipo(df, {'datetime64[s]', 'object'})
                if not campi_data:
                    print("Nessun campo di tipo data trovato nella df.")
                    exit()
                elif len(campi_data) == 1:
                    print(f"\n Campi di tipo data trovati: {campi_data}")
                    campo_data = campi_data[0]
                    data_inizio = chiedi_data("inizio")
                    data_fine = chiedi_data("fine")

                    df[campo_data] = pandas.to_datetime(df[campo_data], errors='coerce')
                    df_filter = df[(df[campo_data] >= data_inizio) & (df[campo_data] <= data_fine)]
                    return df_filter
                    # df_filter = df[(df[campo_numerico] >= valore_min) & (df[campo_numerico] <= valore_max)]
                    # return df_filter
                campo_data = campi_data[validate_input.esegui(f"\n Campi di tipo data trovati: {campi_data}\n Seleziona il numero del campo da filtrare (1-{len(campi_data)}): ", int, minimo=1, massimo=len(campi_data)) - 1]
                data_inizio = chiedi_data("inizio")
                data_fine = chiedi_data("fine")
                df[campo_data] = pandas.to_datetime(df[campo_data], errors='coerce')
                df_filter = df[(df[campo_data] >= data_inizio) & (df[campo_data] <= data_fine)]
                return df_filter
            
        df = switch_filter(tipo)
        return df

    df_filtered = filter_datafield(df)
    return df_filtered

