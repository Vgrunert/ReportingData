import csv
import os
import xml.etree.ElementTree as ET

def csv_to_xml(csv_file_path, xml_file_path, root_tag="root", row_tag="row", delimiter=','):
    """
    Convert a CSV file to an XML file.

    Args:
        csv_file_path (str): Path to the input CSV file.
        xml_file_path (str): Path to the output XML file.
        root_tag (str): Name of the root XML element.
        row_tag (str): Name of each row element.
        delimiter (str): CSV delimiter (default is comma).
    """

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=delimiter)

            # Ensure CSV has headers
            if reader.fieldnames is None:
                raise ValueError("CSV file must have a header row.")

            # Create XML root
            root = ET.Element(root_tag)

            # Add rows to XML
            for row in reader:
                row_elem = ET.SubElement(root, row_tag)
                for key, value in row.items():
                    child = ET.SubElement(row_elem, key)
                    child.text = value if value is not None else ""

        # Write XML to file with pretty formatting
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)  # Python 3.9+ pretty print
        tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

        print(f"✅ Successfully converted '{csv_file_path}' to '{xml_file_path}'.")

    except csv.Error as e:
        raise ValueError(f"Error reading CSV file: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    input_csv = "data.csv"
    output_xml = "data.xml"

    try:
        csv_to_xml(input_csv, output_xml, root_tag="people", row_tag="person", delimiter=',')
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
