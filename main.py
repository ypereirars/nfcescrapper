import argparse
from nfce.services import scrape_invoice
from nfce.utils import save_json
from nfce.database import save


def main(url: str, save_db: bool = True, output: str = None):

    invoice = scrape_invoice(url)

    if save_db:
        try:
            print("Saving to database")
            save(invoice)
        except Exception as e:
            print("Error saving to database")
            print(e)

    if output and output.endswith(".json"):
        print(f"Saving to file {output}")
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
    parser.add_argument("--save-db", action="store_true", help="Save to database")

    args = parser.parse_args()

    main(args.url, args.save_db, args.output)
