from .parsers import NfeParser
from .scrapers import NfeScraper
from .models import NotaFiscalEletronica
from .browsers import get_browser


def read_invoice(url: str) -> NotaFiscalEletronica:
    """Reads an invoice from a given URL.

    Args:
        url (str): URL to scrap.

    Returns:
        NotaFiscalEletronica: invoice data.
    """
    with get_browser() as browser:
        scraper = NfeScraper(NfeParser(), browser)
        invoice = scraper.scrap(url)

        return invoice
