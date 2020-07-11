from processor.NfeProcessor import NfeProcessor
from utils.strcleaner import StrCleaner
import argparse, json, os

parser = argparse.ArgumentParser(description='Download data from a NFe.')

parser.add_argument('--url',  metavar='url', type=str, required=True, 
                    help='URL to download NFe.')

parser.add_argument('--out',  metavar='o', type=str, default="data.json",
                    help='Filename to save data.')

parser.add_argument('--webdriver-path', metavar='wp', type=str, default="chromedriver",
                    help='Chrome webdriver path. If not provided, include webdriver in PATH env vars')

args = parser.parse_args()

processor = NfeProcessor(args.webdriver_path)
data = processor.process(args.url)

with open(args.out, 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
