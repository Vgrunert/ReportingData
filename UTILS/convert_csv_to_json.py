import csv
import json

def csv_to_json(csv_file_path, json_file_path, delimiter=';'):
    encodings_to_try = [
        "utf-8-sig",
        "utf-8",
        "cp1252",
        "latin-1",
    ]

    last_error = None

    for encoding in encodings_to_try:
        try:
            with open(csv_file_path, mode="r", encoding=encoding, newline="") as csv_file:
                reader = csv.DictReader(csv_file, delimiter=delimiter)

                if reader.fieldnames is None:
                    raise ValueError("CSV file has no header row")

                data = list(reader)

            # ✅ Erfolgreich gelesen → JSON schreiben
            with open(json_file_path, mode="w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

            print(
                f"✅ Converted '{csv_file_path}' → '{json_file_path}' "
                f"(encoding erkannt: {encoding})"
            )
            return  # wichtig: abbrechen, sobald es geklappt hat

        except UnicodeDecodeError as e:
            last_error = e
            continue

    # Wenn nichts funktioniert hat
    raise RuntimeError(
        f"Konnte CSV-Encoding nicht bestimmen. Letzter Fehler: {last_error}"
    )
