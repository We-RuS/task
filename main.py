import argparse
from tabulate import tabulate
import csv
from typing import Union, List, Dict


def read_csv(file_path: str = "products.csv") -> List[Dict[str, str]]:
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [line for line in reader]
    except FileNotFoundError:
        print("File not found")


def split_condition(condition: str) -> tuple:
    for i_sym in ("<", ">", "="):
        if i_sym in condition:
            condition = condition.split(i_sym)
            if len(condition) == 2:
                return condition[0], i_sym, condition[1]
    raise ValueError(f"Invalid condition {condition}")


def filter_by_condition(condition: str, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if not split_condition(condition):
        return data
    column, operator, value = split_condition(condition)

    def compare(row: Dict[str, str]) -> bool:
        try:
            condition_value = float(value)
            filter_value = float(row[column])
        except ValueError:
            condition_value = str(value)
            filter_value = str(row[column])

        if operator == '=':
            return condition_value == filter_value
        elif operator == '>':
            return filter_value > condition_value
        elif operator == '<':
            return filter_value < condition_value

    return [row for row in data if compare(row)]


def aggregation(data: List[Dict[str, str]], aggregate_value: str) -> List[Dict[str, Union[str, float]]]:
    aggregate_value = aggregate_value.split('=')
    if len(aggregate_value) != 2:
        raise ValueError(f"Invalid aggregate value: {aggregate_value}")

    column, operator = aggregate_value
    numeric_values = []
    for row in data:
        try:
            numeric_values.append(int(row[column]))
        except ValueError:
            continue

    if not numeric_values:
        return [{'column': "No numeric values to aggregate"}]

    if operator == 'avg':
        result = sum(numeric_values) / len(numeric_values)
    elif operator == 'min':
        result = min(numeric_values)
    elif operator == 'max':
        result = max(numeric_values)
    else:
        raise ValueError(f'Invalid Operator:{operator}')

    return [{'column': column, operator: result}]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Path to CSV file')
    parser.add_argument('--where', help='Filter Condition (e.g. "price>600")')
    parser.add_argument('--aggregate', help='Aggregation condition (e.g. "rating=avg")')
    args = parser.parse_args()

    if args.file:
        data = read_csv(args.file)

    else:
        data = read_csv()

    if args.where:
        filtered_data = filter_by_condition(args.where, data)
        return tabulate(filtered_data, headers='keys', tablefmt='outline')

    if args.aggregate:
        aggregated_data = aggregation(data, args.aggregate)
        return tabulate(aggregated_data, headers='keys', tablefmt='outline')

    else:
        return tabulate(data, headers='keys', tablefmt='outline')


if __name__ == "__main__":
    print(main())
