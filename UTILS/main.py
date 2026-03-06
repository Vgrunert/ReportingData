import convert_csv_to_json
import convert_csv_to_xml


from pathlib import Path

# Define the directory path
csv_path = Path('C:\\Users\\vince\\OneDrive\\Kurse\\BDA_28201055\\ReportingData\\Daten\\CSV')
json_path = Path('C:\\Users\\vince\\OneDrive\\Kurse\\BDA_28201055\\ReportingData\\Daten\\JSON')
xml_path = Path('C:\\Users\\vince\\OneDrive\\Kurse\\BDA_28201055\\ReportingData\\Daten\\XML')

# List all files in the directory
for file in csv_path.iterdir():
    if file.is_file():
        # print(f"File name: {file.name} and File path: {file}")
        # To read the content:
        # content = file.read_text()
        # convert_csv_to_json.csv_to_json(str(file), str(json_path / f"{file.stem}.json"))
        convert_csv_to_xml.csv_to_xml(str(file), str(xml_path / f"{file.stem}.xml"))
