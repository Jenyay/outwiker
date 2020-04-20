from buildtools.linter import LinterResult


def test_result():
    ok = LinterResult.OK
    warn = LinterResult.WARNING
    error = LinterResult.ERROR

    assert (ok & ok) == ok
    assert (ok & warn) == warn
    assert (ok & error) == error
    assert (warn & ok) == warn
    assert (error & ok) == error

    assert (error & error) == error
    assert (error & warn) == error
    assert (error & ok) == error
