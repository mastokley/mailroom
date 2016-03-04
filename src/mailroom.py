# coding=utf-8
from __future__ import print_function, unicode_literals
from builtins import input, open


class DonorData(object):
    def __init__(self):
        """Create empty donor database"""
        self.table = {}

    def all_donor_names(self):
        """Return iterator of donor names"""
        return iter(self.table)

    def donor_history(self, donor_name):
        """Return list of donations or None if empty"""
        return self.table.get(donor_name)

    def add_donation(self, donor_name, amount):
        """create donor if name does not exist"""
        self.table.setdefault(donor_name, []).append(amount)
        """add donation to data"""


def make_report(donors):
    """Print a list of donors, sorted by total historical donation amount"""
    for donor in donors.all_donor_names():

    pass


def main():
    donors = DonorData()
    while main_menu(donors):
        pass


def main_menu(donors):
    user_input = input("""main menu message""")
    if """user asked for report""":
        print(make_report(donors))
    elif """user asked to send a thank you""":
        letter_menu(donors)
    elif """user asked to quit""":
        return False
    return True


def show_donor_list(donors):
    pass


def letter_menu(donors):
    while True:
        user_input = input("""get donor name message""")
        if """user asked to go back""":
            return
        elif """user asked for list""":
            show_donor_list()
            continue

    donor_name = user_input

    while True:
        user_input = input("""get donation amount message""")
        if """user asked to go back""":
            return
        if """input was not a number""":
            print("""not a number message""")

    donation_amount = user_input

    donors.add_donation(donor_name, donation_amount)
    send_thank_you(donor_name, donation_amount)


def send_thank_you(donor_name, donation_amount):
    pass
