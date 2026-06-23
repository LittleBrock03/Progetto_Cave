from dbfread import DBF
import pandas as pd
tabella = DBF(r"C:\Progetto_Cave\esempi\docrig.DBF")

for field in tabella.fields:
    print({field.name}, {field.type})

df = pd.DataFrame(iter(tabella))
df.to_excel(r"C:\Progetto_Cave\export\testt.xlsx", index=False)
