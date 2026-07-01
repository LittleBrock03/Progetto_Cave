# Crea Report

Il progetto produce un solo `Crea_Report.exe` in formato PyInstaller onefile.
I report usano le configurazioni conservate nelle rispettive cartelle release;
i batch centrali selezionano config, sorgente DBF e destinazione.

## Creazione della release

Da PowerShell o dal prompt dei comandi:

```bat
build_release.bat
```

La build locale produce:

```text
release\
`-- Crea_Report.exe
```

Nella cartella condivisa la struttura distribuita è:

```text
Release\
|-- Crea_Report.exe
|-- Batch\
|   |-- _esegui_report.bat
|   |-- run_contabilita_CBR.bat
|   |-- run_report_cave_ICR.bat
|   `-- ...
|-- release_anagrafica_CBR\
|-- release_anagrafica_ICR\
|-- release_contabilita_CBR\
`-- release_report_cave_ICR\
```

Non esistono copie dell'eseguibile o cartelle `_internal` nelle singole
release. I batch in `Release\Batch` richiamano l'EXE nella radice e passano il
percorso della config presente nella cartella release corrispondente. Log,
config, export e file prodotti restano nelle posizioni già utilizzate.

Per l'attività pianificata si usa `Batch\run_report_periodico.bat`, che richiama
`run_tutti_periodico.bat`. Il batch totale esegue sempre tutti i report, anche
quando uno fallisce. Se almeno un report termina con errore, crea sul Desktop
`Crea_Report_ERRORI.txt` con l'elenco dei report non completati e restituisce
codice di uscita `1`; se tutto riesce elimina un'eventuale nota precedente.
