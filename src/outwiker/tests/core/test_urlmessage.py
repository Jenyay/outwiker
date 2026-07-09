from outwiker.core.urlmessage import URLMessage, parse_urlmessage


def test_valid_full_message():
    msg = parse_urlmessage("outwiker://test?foo=bar&baz=123")
    assert isinstance(msg, URLMessage)
    assert msg.protocol == "outwiker"
    assert msg.message_name == "test"
    assert msg.params == {"foo": "bar", "baz": "123"}


def test_message_without_params():
    msg = parse_urlmessage("outwiker://event")
    assert msg.protocol == "outwiker"
    assert msg.message_name == "event"
    assert msg.params == {}


def test_message_with_empty_query():
    msg = parse_urlmessage("outwiker://event?")
    assert msg.message_name == "event"
    assert msg.params == {}


# def test_urlencoded_value():
#     msg = parse_urlmessage("outwiker://test?greeting=Hello%20World&plus=foo+bar")
#     assert msg.message_name == "test"
#     assert msg.params == {"greeting": "Hello World", "plus": "foo bar"}


def test_param_without_value():
    msg = parse_urlmessage("outwiker://test?flag&other=val")
    assert msg.message_name == "test"
    assert msg.params == {"flag": "", "other": "val"}


def test_param_with_empty_value():
    msg = parse_urlmessage("outwiker://test?empty=&keep")
    assert msg.message_name == "test"
    assert msg.params == {"empty": "", "keep": ""}


def test_wrong_protocol():
    # Missing "://"
    assert parse_urlmessage("http//test?x=1") is None
    assert parse_urlmessage("outwiker:/test") is None
    # Empty protocol
    assert parse_urlmessage("://test?x=1") is None
    assert parse_urlmessage("") is None
    assert parse_urlmessage("something") is None


def test_empty_message_name():
    assert parse_urlmessage("outwiker://?x=1") is None
    assert parse_urlmessage("outwiker://") is None


def test_multiple_question_marks():
    # Only the first '?' separates name from params; the rest are part of params
    msg = parse_urlmessage("outwiker://name?x=1?y=2&z=3")
    assert msg.message_name == "name"
    assert msg.params == {"x": "1?y=2", "z": "3"}


def test_trailing_ampersand():
    msg = parse_urlmessage("outwiker://test?a=1&b=2&")
    assert msg.params == {"a": "1", "b": "2"}


def test_empty_pairs_ignored():
    msg = parse_urlmessage("outwiker://test?&&a=1&&b=2&&")
    assert msg.params == {"a": "1", "b": "2"}


# def test_russian_single_param():
#     msg = parse_urlmessage("outwiker://test?msg=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82")
#     assert msg.message_name == "test"
#     assert msg.params == {"msg": "привет"}


# def test_russian_with_plus_as_space():
#     msg = parse_urlmessage(
#         "outwiker://test?msg=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82+%D0%BC%D0%B8%D1%80"
#     )
#     assert msg.message_name == "test"
#     assert msg.params == {"msg": "привет мир"}


def test_expected_protocol_matches():
    msg = parse_urlmessage("outwiker://test?foo=bar", expected_protocol="outwiker")
    assert msg is not None
    assert msg.protocol == "outwiker"
    assert msg.message_name == "test"
    assert msg.params == {"foo": "bar"}


def test_expected_protocol_does_not_match():
    assert (
        parse_urlmessage("outwiker://test?foo=bar", expected_protocol="custom") is None
    )
    assert parse_urlmessage("custom://test", expected_protocol="outwiker") is None


def test_expected_protocol_none_behavior():
    # With expected_protocol=None (default), any protocol is accepted
    msg1 = parse_urlmessage("outwiker://event", expected_protocol=None)
    assert msg1 is not None
    assert msg1.protocol == "outwiker"


def test_expected_protocol_with_missing_protocol():
    # URL without "://" should return None regardless of expected_protocol
    assert parse_urlmessage("invalid", expected_protocol="outwiker") is None
    assert parse_urlmessage("invalid", expected_protocol=None) is None


def test_expected_protocol_case_sensitive():
    # Protocols are case-sensitive (exact match)
    assert parse_urlmessage("OutWiker://test", expected_protocol="outwiker") is None

    # But if we don't specify expected, it works with the extracted protocol
    msg = parse_urlmessage("OutWiker://test")
    assert msg.protocol == "OutWiker"
