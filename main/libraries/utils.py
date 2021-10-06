import logging
from typing import Tuple
from urllib.parse import unquote

logger = logging.getLogger(__name__)


def parse_street_and_number(street_and_number: str) -> Tuple[str, str]:
    """
    Vezme jeden string (ulice a ČP dohromady) a snaží se to parsovat na dva.
    """
    for i, c in enumerate(street_and_number):
        # najdi prvni cislici v ulice_cislo
        # přeskočím první 3 písmena, abych nechytal čísla jako 1. pluku apod.
        if c.isdigit() and i not in [1, 2, 3]:
            return street_and_number[:i - 1], street_and_number[i:]

    # pokud nic nenajdu tak vrátím v ulici všechno a do ČP nic
    return street_and_number, ''


def parse_first_and_last_name(first_and_last_name: str) -> Tuple[str, str]:
    """
    Vezme jeden string (jméno a příjmení dohromady) a snaží se to parsovat na dva.
    """
    # todo fixnout problém s titulem za jménem
    try:
        return ' '.join(first_and_last_name.split()[:-1]), first_and_last_name.split()[-1]
    except IndexError:
        return first_and_last_name, ''


def get_location_format(number=None, street=None, zip_code=None, city=None):
    adrress = ""

    if street:
        adrress += street
        if not number and city:
            adrress += ","
        adrress += " "

    if number:
        if street:
            adrress += number
            if city:
                adrress += ", "
    if city:
        adrress += city
        # for villages without street put number after city name
        if not street and number:
            adrress += " "
            adrress += number
        if zip_code:
            adrress += " "
    if zip_code:
        adrress += zip_code
    return adrress


def decode_url(url: str):
    return unquote(url)
