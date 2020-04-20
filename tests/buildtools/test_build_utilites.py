# -*- coding: utf-8 -*-

from buildtools.utilites import tobool


def test_tobool():
    assert tobool(1)
    assert tobool(True)
    assert tobool(u'1')
    assert tobool(u'True')
    assert tobool('True')
    assert tobool(u'true')
    assert tobool('true')

    assert not tobool(0)
    assert not tobool(u'0')
    assert not tobool(False)
    assert not tobool(u'False')
    assert not tobool('False')
    assert not tobool(u'false')
    assert not tobool('false')
