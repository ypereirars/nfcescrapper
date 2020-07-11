from processor.NfeProcessor import NfeProcessor
from utils.strcleaner import StrCleaner
import argparse, json, os, csv

parser = argparse.ArgumentParser(description='Download data from a NFe.')

parser.add_argument('--url',  metavar='url', type=str, required=True, 
                    help='URL to download NFe.')

parser.add_argument('--format',  metavar='o', type=str, default="json",
                    help='Whether to export as csv or json. Defaults to json')

parser.add_argument('--out',  metavar='o', type=str, default="data",
                    help='Filename to save data.')

parser.add_argument('--webdriver-path', metavar='wp', type=str, default="chromedriver",
                    help='Chrome webdriver path. If not provided, include webdriver in PATH env vars')

args = parser.parse_args()

processor = NfeProcessor(args.webdriver_path)
data = processor.process(args.url)

if args.format == "json":
    with open(args.out, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

elif args.format == "csv":
    csv_columns = list()
    header_keys = [k for k in data.keys()]
    header_keys.remove("items")
    
    csv_columns.extend(header_keys)

    assert len(data["items"]) > 0, "Data contain no item"

    csv_columns.extend(data["items"][0].keys())

    try:
        with open(args.out, 'w', encoding='utf-8', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
            writer.writeheader()
            header = dict(data)
            del header["items"]
            items = data["items"]
            
            dict_data = [{**i, **header} for i in items]

            for d in dict_data:
                writer.writerow(d)
    except IOError:
        print("I/O error")

else:
    print("Format not recognized")