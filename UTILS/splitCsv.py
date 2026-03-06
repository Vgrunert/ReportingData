import csv
import argparse
import os

def split_csv_into_parts(file_path, parts=3, encoding="utf-8", delimiter=","):
    if not os.path.exists(file_path):
        print(f"Fehler: Datei {file_path} nicht gefunden.")
        return

    if parts < 2:
        print("Fehler: '--parts' muss mindestens 2 sein.")
        return

    # CSV einlesen
    with open(file_path, mode="r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(
            f,
            delimiter=delimiter,
            restkey="__extra__",     # falls Zeile mehr Spalten hat als Header
            restval=""               # falls Zeile weniger Spalten hat als Header
        )
        fieldnames = reader.fieldnames
        if not fieldnames:
            print("Fehler: Konnte keinen Header (Spaltennamen) finden.")
            return

        rows = list(reader)

    total = len(rows)
    if total == 0:
        print("Hinweis: Datei enthält keine Datenzeilen (nur Header).")
        # trotzdem leere Teile schreiben
        base_name = os.path.splitext(file_path)[0]
        for i in range(parts):
            out = f"{base_name}_part_{i+1}.csv"
            with open(out, mode="w", encoding=encoding, newline="") as wf:
                writer = csv.DictWriter(wf, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
            print(f"Gespeichert: 0 Zeilen in {out}")
        return

    # ungefähr gleich große Chunkgrößen (Rest wird am Anfang verteilt)
    base = total // parts
    rest = total % parts
    sizes = [base + (1 if i < rest else 0) for i in range(parts)]

    base_name = os.path.splitext(file_path)[0]
    start = 0

    for i, size in enumerate(sizes):
        end = start + size
        chunk = rows[start:end]
        start = end

        output_filename = f"{base_name}_part_{i+1}.csv"
        with open(output_filename, mode="w", encoding=encoding, newline="") as wf:
            writer = csv.DictWriter(
                wf,
                fieldnames=fieldnames,
                delimiter=delimiter,
                extrasaction="ignore"   # ignoriert Keys, die nicht in fieldnames sind (z.B. None oder __extra__)
            )
            writer.writeheader()
            writer.writerows(chunk)

        print(f"Gespeichert: {len(chunk)} Zeilen in {output_filename}")

    print(f"Fertig. Total: {total} Zeilen in {parts} Dateien aufgeteilt: {sizes}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Teilt eine CSV-Datei in ungefähr gleich große Teile (nach Zeilenanzahl)."
    )
    parser.add_argument("file", help="Pfad zur CSV-Datei")
    parser.add_argument("--parts", type=int, default=3, help="Anzahl Teile (Standard: 3)")
    parser.add_argument("--encoding", default="utf-8", help="Datei-Encoding (Standard: utf-8)")
    parser.add_argument("--delimiter", default=",", help="Spaltentrenner, z.B. ';' oder ',' (Standard: ',')")

    args = parser.parse_args()
    split_csv_into_parts(
        args.file,
        parts=args.parts,
        encoding=args.encoding,
        delimiter=args.delimiter
    )