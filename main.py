import argparse
from nfce.services import read_invoice
from nfce.utils import save_json


def main(url: str, output: str = None):

    invoice = read_invoice(url)

    if output and output.endswith(".json"):
        save_json(invoice, output)

    return invoice


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download data from a NFe.")

    parser.add_argument("url", metavar="url", type=str, help="URL to download the NFe.")
    parser.add_argument(
        "--output",
        "-o",
        metavar="path",
        type=str,
        default=None,
        help="File path location where to save data. The file path must have a .json extension.",
    )

    args = parser.parse_args()

    main(args.url, args.output)
