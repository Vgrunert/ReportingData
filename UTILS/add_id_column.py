import pandas as pd

def add_id_column(input_file, output_file, id_column_name='id'):
    try:
        # 1. Load the CSV
        df = pd.read_csv(input_file)

        # 2. Create the ID column
        # range(1, len(df) + 1) creates 1, 2, 3...
        # insert(location, column_name, values)
        df.insert(0, id_column_name, range(1, len(df) + 1))

        # 3. Save to a new CSV
        df.to_csv(output_file, index=False)
        print(f"Success! Saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
add_id_column('input.csv', 'output_with_ids.csv')