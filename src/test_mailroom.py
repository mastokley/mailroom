# coding=utf-8
from __future__ import unicode_literals


def test_foo():
    assert 1 == 1


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


def test_make_report():
    import mailroom
    dd = mailroom.DonorData()
    dd.add_donation("John Smith", 50)
    dd.add_donation("John Smith", 500)
    dd.add_donation("Sally Smith", 500)

    assert mailroom.make_report(dd) == (
        "John Smith:\n"
        "    50, 500\n"
        "    550 total\n"
        "Sally Smith:\n"
        "    500\n"
        "    500 total\n"
    )
