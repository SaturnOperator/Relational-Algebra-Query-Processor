import argparse
import json

# Functions to load and save data from JSON
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Checks if a value satisfies the given condition
def satisfies_condition(value, operator, condition_value):
    try:
        condition_value = type(value)(condition_value)
    except ValueError:
        return False

    if operator == '>':
        return value > condition_value
    elif operator == '>=':
        return value >= condition_value
    elif operator == '<':
        return value < condition_value
    elif operator == '<=':
        return value <= condition_value
    elif operator == '==':
        return value == condition_value
    else:
        return False

# Selection Operation
def select(table, conditions, data):
    if table not in data:
        print(f"Table '{table}' not found.")
        return []

    selected_data = []
    for entry in data[table]:
        add_entry = True
        for condition in conditions:
            if '>' in condition  and not '>=' in condition:
                col, value = condition.split('>', 1)
                if not satisfies_condition(entry.get(col, None), '>', value):
                    add_entry = False
                    break
            elif '>=' in condition:
                col, value = condition.split('>=', 1)
                if not satisfies_condition(entry.get(col, None), '>=', value):
                    add_entry = False
                    break
            elif '<' in condition and not '<=' in condition:
                col, value = condition.split('<', 1)
                if not satisfies_condition(entry.get(col, None), '<', value):
                    add_entry = False
                    break
            elif '<=' in condition:
                col, value = condition.split('<=', 1)
                if not satisfies_condition(entry.get(col, None), '<=', value):
                    add_entry = False
                    break
            elif '==' in condition:
                col, value = condition.split('==', 1)
                if not satisfies_condition(entry.get(col, None), '==', value):
                    add_entry = False
                    break

        # Add the column if a criteria/condition if given and satisfied 
        if add_entry:
            selected_entry = {col.split('>')[0]: entry[col.split('>')[0]] for col in conditions if '>' not in col and col.split('>')[0] in entry}
            if selected_entry:
                selected_data.append(selected_entry)

    if not selected_data:
        print(f"No data found for conditions {conditions} in table '{table}'.")
    
    return selected_data

# Selection and Set Operation
# built on the select operation
def selection_and_set(table, conditions, set_column, set_value, data):
    if table not in data:
        print(f"Table '{table}' not found.")
        return []

    updated = False
    for entry in data[table]:
        add_entry = True
        for condition in conditions:
            if '>' in condition  and not '>=' in condition:
                col, value = condition.split('>', 1)
                if not satisfies_condition(entry.get(col, None), '>', value):
                    add_entry = False
                    break
            elif '>=' in condition:
                col, value = condition.split('>=', 1)
                if not satisfies_condition(entry.get(col, None), '>=', value):
                    add_entry = False
                    break
            elif '<' in condition and not '<=' in condition:
                col, value = condition.split('<', 1)
                if not satisfies_condition(entry.get(col, None), '<', value):
                    add_entry = False
                    break
            elif '<=' in condition:
                col, value = condition.split('<=', 1)
                if not satisfies_condition(entry.get(col, None), '<=', value):
                    add_entry = False
                    break
            elif '==' in condition:
                col, value = condition.split('==', 1)
                if not satisfies_condition(entry.get(col, None), '==', value):
                    add_entry = False
                    break

        if add_entry:
            if set_column in entry:
                try:
                    entry[set_column] = type(entry[set_column])(set_value)
                    updated = True
                except ValueError:
                    print(f"Type mismatch for column '{set_column}'.")
    
    if updated:
        save_data('data.json', data)
        print(f"Updated table '{table}'.")
    else:
        print(f"No data updated for table '{table}' with conditions {conditions}.")

# Join Operation
def join(table1, table2, join_column, data):
    if table1 not in data:
        print(f"Table name '{table1}' not found.")
        return []

    if  table2 not in data:
        print(f"Table name '{table2}' not found.")
        return []

    table1_data = data[table1]
    table2_data = data[table2]

    # Perform the join
    joined_data = []
    for row1 in table1_data:
        for row2 in table2_data:
            if row1.get(join_column, None) == row2.get(join_column, None):
                # Merging two dictionaries
                joined_row = {**row1, **row2}
                joined_data.append(joined_row)

    return joined_data

# Parse Arguments
# Use argparse to parse the syntax
def parse_arguments():
    parser = argparse.ArgumentParser(description='Relational Algebra Query Processor')
    parser.add_argument('--select', nargs='+', help='Perform a selection operation')
    parser.add_argument('--set', nargs=2, metavar=('COLUMN', 'VALUE'), help='Set a value in a column')
    parser.add_argument('--join', nargs=3, metavar=('TABLE1', 'TABLE2', 'COLUMN'), help='Join two tables')
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    data = load_data('data.json')

    if args.select and len(args.select) >= 2:
        table = args.select[0]
        conditions = args.select[1:]
        if args.set:
            set_column, set_value = args.set
            selection_and_set(table, conditions, set_column, set_value, data)
        else:
            selected_data = select(table, conditions, data)  # Selection logic
            print(selected_data, ":", "\n")

            for i in selected_data:
                print(i)

    elif args.join:
        table1, table2, join_column = args.join
        joined_data = join(table1, table2, join_column, data)
        for item in joined_data:
            print(item)
    else:
        print("Invalid selection command. Please specify a table and conditions.")

if __name__ == "__main__":
    main()
