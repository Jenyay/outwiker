from buildtools.linter import LinterStatus


def test_status():
    ok = LinterStatus.OK
    warn = LinterStatus.WARNING
    error = LinterStatus.ERROR

    assert (ok & ok) == ok
    assert (ok & warn) == warn
    assert (ok & error) == error
    assert (warn & ok) == warn
    assert (error & ok) == error

    assert (error & error) == error
    assert (error & warn) == error
    assert (error & ok) == error
