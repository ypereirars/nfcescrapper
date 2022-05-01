from nfce import NFCeParser, NfeScrapper
import argparse, json, csv


def main(args):
    parser = NFCeParser()
    processor = NfeScrapper(parser, args.webdriver_path)
    data = processor.get(args.url)

    output_path = f'{args.out}.{args.format}'
    with open(output_path, 'w', encoding='utf-8') as outfile:
        if args.format == "json":
            data = data.serialize()
            json.dump(data, outfile, ensure_ascii=False, indent=4)
        elif args.format == "csv":
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

    parser.add_argument('--url',  metavar='url', type=str, required=True,
                        help='URL to download NFe.')

    parser.add_argument('--format',  metavar='o', type=str, default='csv', choices=['json', 'csv'],
                        help='Whether to export as csv or json. Defaults to json')

    parser.add_argument('--out',  metavar='o', type=str, default="data",
                        help='Filename to save data.')

    parser.add_argument('--webdriver-path', metavar='wp', type=str, default='chromedriver',
                        help='Chrome webdriver path. If not provided, include webdriver in PATH env vars')

    args = parser.parse_args()

    main(args)
