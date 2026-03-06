import json
import argparse
import os

def split_json(file_path, split_years):
    # 1. Load the data
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Sort split years to ensure logic works (ascending)
    split_years = sorted([int(y) for y in split_years])
    
    # 2. Create "buckets" for the groups
    # If we have 2 split years (e.g., 2020, 2022), we need 3 groups:
    # Group 1: < 2020
    # Group 2: 2020 to 2021
    # Group 3: >= 2022
    num_groups = len(split_years) + 1
    groups = [[] for _ in range(num_groups)]

    for item in data:
        year = int(item.get('yearID'))
        if year is None:
            continue
        
        # Determine which group the year belongs to
        placed = False
        for i, split_year in enumerate(split_years):
            if year < split_year:
                groups[i].append(item)
                placed = True
                break
        
        if not placed:
            groups[-1].append(item)

    # 3. Save the files
    base_name = os.path.splitext(file_path)[0]
    for i, group_data in enumerate(groups):
        output_filename = f"{base_name}_part_{i+1}.json"
        with open(output_filename, 'w') as f:
            json.dump(group_data, f, indent=4)
        print(f"Saved {len(group_data)} items to {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a JSON file by year ranges.")
    parser.add_argument("file", help="Path to the source JSON file")
    parser.add_argument("years", nargs="+", type=int, help="The years to split on (e.g., 2020 2022)")

    args = parser.parse_args()
    
    split_json(args.file, args.years)