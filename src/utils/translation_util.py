"""Module for translation utilities"""
import sys
import csv
import pandas as pd


def read_csv(file_path):
    """Reads a CSV file and returns a DataFrame."""
    return pd.read_csv(file_path)


def collect_texts(df, columns_to_drop=None):
    """Collects all texts from a DataFrame."""

    src_df = df.copy()
    if columns_to_drop:
        src_df.drop(columns=columns_to_drop, inplace=True)

    texts = []
    for column in src_df.columns:
        texts.extend(src_df[column].unique().tolist())

    texts = list(set(texts))

#    texts_dict = {text: "TRANSLATE" for text in texts}

#    print(texts_dict)
    return texts


def append_to_csv(file_path, data):
    """Appends a dictionary to a CSV file."""
    existing_data = {}
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_data = {rows[0]: rows[1] for rows in reader}
    except FileNotFoundError:
        print("Output file not found, exiting")
        sys.exit(1)

    with open(file_path, "a", encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            if key not in existing_data:
                writer.writerow([key, value])


def lists_to_dict(texts1, texts2):
    """Converts two lists to a dictionary."""
    texts = texts1 + texts2

    texts_dict = {text: "TRANSLATE" for text in texts}

    return texts_dict


def write_csv(file_path, data):
    """Writes a dictionary to a CSV file."""
    with open(file_path, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])


def main():
    """Main entry point for the application."""

    if len(sys.argv) < 2:
        print("Usage: python script.py <source1.csv> <sourve2.csv> <output.csv>")
        sys.exit(1)

    sourcefile1 = sys.argv[1]
    sourcefile2 = sys.argv[2]
    outputfile = sys.argv[3]

    inc_df = read_csv(sourcefile1)
    exp_df = read_csv(sourcefile2)

    texts1 = collect_texts(inc_df, columns_to_drop=["total"])
    texts2 = collect_texts(exp_df, columns_to_drop=["total"])

    texts_dict = lists_to_dict(texts1, texts2)

    append_to_csv(outputfile, texts_dict)
    # write_csv(outputfile, texts_dict)


if __name__ == "__main__":
    main()
