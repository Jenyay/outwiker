# -*- coding: utf-8 -*-

from buildtools.utilites import tobool


def test_tobool():
    assert tobool(1)
    assert tobool(True)
    assert tobool('1')
    assert tobool('True')
    assert tobool('True')
    assert tobool('true')
    assert tobool('true')

    assert not tobool(0)
    assert not tobool('0')
    assert not tobool(False)
    assert not tobool('False')
    assert not tobool('False')
    assert not tobool('false')
    assert not tobool('false')
