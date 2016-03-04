# coding=utf-8
from __future__ import print_function, unicode_literals
from builtins import input

import re
import sqlite3

from tabulate import tabulate


NUMBER_TEST = re.compile(r"^\$?(\d+(\.\d\d?)?)$")
DB_PATH = "donations.db"


class DonorData(object):
    def __init__(self, filename=":memory:"):
        """Create empty donor database"""
        self.db = sqlite3.Connection(filename)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS donations (
                donor TEXT NOT NULL COLLATE NOCASE,
                amount REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS ix_donors ON donations(donor);
        """)

    def all_donor_names(self):
        """Return iterator of donor names"""
        return (donor for (donor,) in self.db.execute(
            "SELECT DISTINCT donor FROM donations"
        ))

    def donor_history(self, donor_name):
        """Return list of donations or None if empty"""
        return list(amount for (amount,) in self.db.execute(
            "SELECT amount FROM donations WHERE donor = ?",
            (donor_name,)
        )) or None

    def add_donation(self, donor_name, amount):
        """create donor if name does not exist"""
        with self.db:
            self.db.execute(
                "INSERT INTO donations (donor, amount) "
                "VALUES (?, ?)",
                (donor_name, amount)
            )


def make_report(donors):
    """Print a list of donors, sorted by total historical donation amount"""
    donor_info = []
    for donor_name in donors.all_donor_names():
        history = donors.donor_history(donor_name)
        total = float(sum(history))
        donation_count = len(history)
        average = float(total / donation_count,)
        donor_info.append((total, donor_name, donation_count, average))

    donor_info.sort(reverse=True)

    return tabulate(
        donor_info,
        headers=[
            "Total", "Donor", "Number of donations", "Average donation"
        ],
        tablefmt='grid',
        floatfmt='.2f',
    )


def main_menu(donors):
    while True:
        user_input = input(
            "MAILROOM MADNESS (1: 'report', 2: 'thank', 'quit'): "
        ).strip()

        if user_input.lower() in ("report", "1"):
            print(make_report(donors))
        elif user_input.lower() in ("thank", "2"):
            letter_menu(donors)
        elif user_input.lower() in ("quit", "exit", "q", ":q"):
            return


def make_donor_list(donors):
    return (
        "\n"
        "Donors:\n"
        "-------\n"
    ) + "\n".join(sorted(
        donors.all_donor_names(),
        key=lambda x: x.lower()  # sort case-insensitive
    ))


def parse_donation_amount(user_input):
    """
    Accept a string and return the amount of money it represents
    if it was valid, or None if it wasn't
    """
    match = NUMBER_TEST.match(user_input)
    if match:
        return float(match.group(1))
    else:
        # input was not a number
        return None


def letter_menu(donors):
    donor_name = None  # for static inspections
    donation_amount = None

    while True:
        user_input = input("Input donor name (or 'back', 'list'): ").strip()
        if user_input.lower() == "back":
            return
        elif user_input.lower() == "list":
            print(make_donor_list(donors))
            continue
        elif not user_input:
            # empty string, ask again
            continue
        # user_input is now the donor's name
        donor_name = user_input
        break

    while True:
        user_input = input("Enter donation amount ('back'): ").strip()
        if user_input.lower() == "back":
            return  # back to main menu
        if not user_input:
            continue

        donation_amount = parse_donation_amount(user_input)
        if not donation_amount:
            print("'{}' is not a valid donation amount!".format(user_input))
            continue
        else:
            break

    donors.add_donation(donor_name, donation_amount)
    print(make_thank_you(donor_name, donation_amount))


def make_thank_you(donor_name, donation_amount):
    return """Dear {0},

    Thank you for your generous donation of ${1:.2f}. Something something,
etc., please do it again immediately except with more money.

Regards,

DonationCorp Ltd.""".format(donor_name, donation_amount)


def main():
    """Main CLI method"""
    donors = DonorData(DB_PATH)
    main_menu(donors)


if __name__ == "__main__":
    main()
