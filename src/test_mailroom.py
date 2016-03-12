# coding=utf-8
from __future__ import unicode_literals

import pytest
from tabulate import tabulate


def test_foo():
    assert 1 == 1
    assert "asdf   asfda".split() == ["asdf", "asfda"]


TEST_NUMBERS = [
    ("", None),
    ("asfd", None),
    ("333333w", None),
    ("33333333", 33333333),
    ("3.50", 3.5),
    ("$3.50", 3.5),
    ("$$3.50", None),
    ("$3.500", None),
    ("d444", None),
    ("nan", None),
    ("inf", None),
    ("-3.50", None),
    ("$-3.50", None),
    ("-$3.50", None),
    (".50", None),
    ("0.50", .5),
    ("0", 0),
]


@pytest.fixture(scope="module")
def donordata():
    from mailroom import DonorData
    return DonorData()


@pytest.mark.parametrize(("string", "expected"), TEST_NUMBERS)
def test_parse_donation_amount(string, expected):
    from mailroom import parse_donation_amount
    if expected is None:
        assert parse_donation_amount(string) is None
    else:
        assert parse_donation_amount(string) == expected


TEST_DONATIONS = [
    (
        ("John Smith", 50),
        {"John Smith"},
        {"John Smith": [50], "Sally Smith": None}
    ),
    (
        ("John Smith", 500),
        {"John Smith"},
        {"John Smith": [50, 500], "Sally Smith": None}
    ),
    (
        ("Sally Smith", 500),
        {"John Smith", "Sally Smith"},
        {"John Smith": [50, 500], "Sally Smith": [500]}
    )
]


@pytest.mark.parametrize(("add", "expected_names", "expected_history"), TEST_DONATIONS)
def test_donor_table_functionality(donordata, add, expected_names, expected_history):
    donordata.add_donation(*add)
    assert set(donordata.all_donor_names()) == expected_names
    for name, history in expected_history.items():
        assert donordata.donor_history(name) == history


TEST_LISTS = [

]


def test_make_donor_list():
    from mailroom import DonorData, make_donor_list
    dd = DonorData()
    assert make_donor_list(dd) == (
        "\n"
        "Donors:\n"
        "-------\n"
    )
    dd.add_donation("John Smith", 50)
    assert make_donor_list(dd) == (
        "\n"
        "Donors:\n"
        "-------\n"
        "John Smith"
    )

    dd.add_donation("John Smith", 500)
    assert make_donor_list(dd) == (
        "\n"
        "Donors:\n"
        "-------\n"
        "John Smith"
    )

    dd.add_donation("Sally Smith", 500)
    assert make_donor_list(dd) == (
        "\n"
        "Donors:\n"
        "-------\n"
        "John Smith\n"
        "Sally Smith"
    )

    dd.add_donation("aaaaa", 3434)
    assert make_donor_list(dd) == (
        "\n"
        "Donors:\n"
        "-------\n"
        "aaaaa\n"
        "John Smith\n"
        "Sally Smith"
    )


def test_make_report():
    import mailroom
    dd = mailroom.DonorData()
    dd.add_donation("John Smith", 50)
    dd.add_donation("John Smith", 500)
    dd.add_donation("Sally Smith", 500)
    assert mailroom.make_report(dd) == tabulate(
        (
            (550.0, "John Smith", 2, 275.0),
            (500.0, "Sally Smith", 1, 500.0),
        ),
        headers=[
            "Total", "Donor", "Number of donations", "Average donation"
        ],
        tablefmt='grid',
        floatfmt='.2f',
    )


def test_make_thank_you():
    from mailroom import make_thank_you
    assert make_thank_you("asdfSDF", 343423.2399999) == """Dear asdfSDF,

    Thank you for your generous donation of $343423.24. Something something,
etc., please do it again immediately except with more money.

Regards,

DonationCorp Ltd."""
