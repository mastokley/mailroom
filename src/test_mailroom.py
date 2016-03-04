# coding=utf-8
from __future__ import unicode_literals

from tabulate import tabulate


def test_foo():
    assert 1 == 1
    assert "asdf   asfda".split() == ["asdf", "asfda"]


def test_parse_donation_amount():
    from mailroom import parse_donation_amount
    assert parse_donation_amount("") is None
    assert parse_donation_amount("asfd") is None
    assert parse_donation_amount("333333w") is None
    assert parse_donation_amount("33333333") == 33333333
    assert parse_donation_amount("3.50") == 3.5
    assert parse_donation_amount("$3.50") == 3.5
    assert parse_donation_amount("$$3.50") is None
    assert parse_donation_amount("$3.500") is None
    assert parse_donation_amount("d444") is None
    assert parse_donation_amount("nan") is None
    assert parse_donation_amount("inf") is None
    assert parse_donation_amount("-3.50") is None
    assert parse_donation_amount("$-3.50") is None
    assert parse_donation_amount("-$3.50") is None
    assert parse_donation_amount(".50") is None
    assert parse_donation_amount("0.50") == .5
    assert parse_donation_amount("0") == 0


def test_donor_table_functionality():
    import mailroom
    dd = mailroom.DonorData()

    dd.add_donation("John Smith", 50)
    assert set(dd.all_donor_names()) == {"John Smith"}
    assert dd.donor_history("John Smith") == [50]
    assert dd.donor_history("Sally Smith") is None

    dd.add_donation("John Smith", 500)
    assert set(dd.all_donor_names()) == {"John Smith"}
    assert dd.donor_history("John Smith") == [50, 500]
    assert dd.donor_history("Sally Smith") is None

    dd.add_donation("Sally Smith", 500)
    assert set(dd.all_donor_names()) == {"John Smith", "Sally Smith"}
    assert dd.donor_history("John Smith") == [50, 500]
    assert dd.donor_history("Sally Smith") == [500]

    return dd


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
