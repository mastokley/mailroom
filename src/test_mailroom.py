# coding=utf-8


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
