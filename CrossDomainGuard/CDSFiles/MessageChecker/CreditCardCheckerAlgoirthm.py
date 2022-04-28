import re


def sum_digits(n):
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


# Validate card number using Luhn's checksum algorithm
def check_card_number(card_number):
    card_number_list = list(map(int, list(card_number.replace(" ", ""))))
    odd_card_number = card_number_list[1::2]
    even_card_number = [sum_digits(digit * 2) for digit in card_number_list[::2]]
    checksum = sum([x + y for x, y in zip(odd_card_number, even_card_number)])
    return checksum % 2 == 0


# get the card issuer based on card number
def check_card_issuer(card_number):
    card_number = card_number.replace(" ", "")
    issuer_dict = {
        "Mastercard": "^5[1-5][0-9]{14}$}",
        "Visa Card": "^4[0-9]{12}(?:[0-9]{3})?$",
        "Visa Master Card": "^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$"
    }
    for card, regex in issuer_dict.items():
        if re.search(regex, card_number):
            return card


def check_cvv(card_cvv, card_issuer):
    return len(card_cvv) == 3


def check_valid_card(card_number, card_cvv):
    return check_card_issuer(card_number) and check_card_number(card_number) and check_cvv(card_cvv, check_card_issuer(card_number))
