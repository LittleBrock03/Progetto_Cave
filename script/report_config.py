import json
from pathlib import Path


def carica(percorso, nome_report=None):
    percorso = Path(percorso)
    with open(percorso, "r", encoding="utf-8") as f:
        config = json.load(f)

    report_nome = nome_report or config.get("default_report")
    reports = config.get("reports", {})
    datasets = config.get("datasets", {})

    def prepara_report(nome):
        if nome not in reports:
            disponibili = ", ".join(sorted(reports))
            raise ValueError(f"Report '{nome}' non configurato. Disponibili: {disponibili}")

        report_preparato = reports[nome].copy()
        dataset_nome = report_preparato.get("dataset")
        if dataset_nome not in datasets:
            disponibili = ", ".join(sorted(datasets))
            raise ValueError(f"Dataset '{dataset_nome}' non configurato. Disponibili: {disponibili}")

        report_preparato["dataset_config"] = datasets[dataset_nome]
        report_preparato["name"] = nome
        return report_preparato

    if report_nome not in reports:
        disponibili = ", ".join(sorted(reports))
        raise ValueError(f"Report '{report_nome}' non configurato. Disponibili: {disponibili}")

    report = prepara_report(report_nome)
    report["_config_dir"] = percorso.resolve().parent
    extra_sheets = []
    for extra_sheet in report.get("extra_sheets", []):
        extra_report = prepara_report(extra_sheet["report"])
        extra_report["_config_dir"] = percorso.resolve().parent
        override = {
            chiave: valore
            for chiave, valore in extra_sheet.items()
            if chiave != "report"
        }
        extra_report.update(override)
        extra_sheets.append(extra_report)

    report["extra_sheets"] = extra_sheets
    return report
