import os
import csv
import json
import argparse
from nfce import NFCeParser, NfeScrapper


def main(args):
    parser = NFCeParser()
    processor = NfeScrapper(parser, wait_timeout=10)

    data = processor.get(args.url)

    if data is None:
        print("No data found")
        return 1

    if args.output is None:
        print(data.serialize())
        return 0

    output_path, output_format = get_output_path(args)

    return export_data(data, output_path, output_format)


def get_output_path(args):
    _, ext = os.path.splitext(args.output)

    if ext == '':
        output_format = str(args.format).lower()
        output_path = os.path.join(args.output, f'data.{args.format}')
    else:
        output_format = str(ext.strip('.')).lower()
        output_path = args.output

    return output_path, output_format


def export_data(data, output_path, output_format):
    with open(output_path, 'w', encoding='utf-8') as outfile:
        if output_format == 'json':
            data = data.serialize()
            json.dump(data, outfile, ensure_ascii=False, indent=4)
            return 0
        elif output_format == 'csv':
            dump_csv(data, outfile)
            return 0
        else:
            print(f"Unknown format: {output_format}")
            return 1


def dump_csv(data, outfile):
    writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    rows = data.to_csv()
    write_header = True
    for header, row in rows:
        if write_header:
            writer.writerow(header)
            write_header = False

        writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download data from a NFe.')

    parser.add_argument('url',  metavar='url', type=str, help='URL to download the NFe.')
    parser.add_argument('--format', '-f', metavar='format', type=str, default='json', choices=['json', 'csv'],
                        help='Output file format wich may either be json or csv.  Default to `json`.')
    parser.add_argument('--output', '-o',  metavar='path', type=str, default=None,
                        help='File path location where to save data. If path is a folder, than the output will be saved'
                        ' in <path>/data.<format> where <format> is the same as the --format option. However if path is'
                        ' a file, than the output will be saved in <path>. If `None`, then only prints the result to '
                        'console.')

    args = parser.parse_args()  

    main(args)
