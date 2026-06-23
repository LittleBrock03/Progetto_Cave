import json


def carica(percorso, nome_report=None):
    with open(percorso, "r", encoding="utf-8") as f:
        config = json.load(f)

    report_nome = nome_report or config.get("default_report")
    reports = config.get("reports", {})
    if report_nome not in reports:
        disponibili = ", ".join(sorted(reports))
        raise ValueError(f"Report '{report_nome}' non configurato. Disponibili: {disponibili}")

    report = reports[report_nome].copy()
    dataset_nome = report.get("dataset")
    datasets = config.get("datasets", {})
    if dataset_nome not in datasets:
        disponibili = ", ".join(sorted(datasets))
        raise ValueError(f"Dataset '{dataset_nome}' non configurato. Disponibili: {disponibili}")

    report["dataset_config"] = datasets[dataset_nome]
    report["name"] = report_nome
    return report
