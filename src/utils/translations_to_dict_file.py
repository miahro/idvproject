"""Small utility to convert translations csv file to python dictionary file"""
import sys
import csv


def csv_to_python_dict(filename, output_filename):
    """reads translation csv file and writes a dictionary with translations to a Python file"""

    # pylint: disable=R0801
    with open(filename, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        data_dict = {}
        for i, row in enumerate(reader, start=1):
            try:
                key = row[0].strip('"')
                value = row[1].strip('"')
                if key in data_dict:
                    print(f"Duplicate key on line {i}: {row}")
                data_dict[key] = value
            except IndexError:
                print(f"IndexError on line {i}: {row}")

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write("translations = {\n")
        for key, value in data_dict.items():
            outfile.write(f'  {repr(key)}: {repr(value)},\n')
        outfile.write("}\n")


def main():
    """Main entry point for the application."""

    if len(sys.argv) < 2:
        print("Usage: python script.py <source.csv> <output.py>")
        sys.exit(1)

    sourcefile = sys.argv[1]
    outputfile = sys.argv[2]

    csv_to_python_dict(sourcefile, outputfile)


if __name__ == '__main__':
    main()
