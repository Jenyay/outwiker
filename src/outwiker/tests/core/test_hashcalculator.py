import datetime
import os

from outwiker.core.application import Application
from outwiker.core.hashcalculator import SimpleHashCalculator
from outwiker.core.tree import WikiPage
from outwiker.tests.fixtures import application, wikipage
from outwiker.tests.utils import copy_test_files_to_attachments

def set_file_times(file_path, new_datetime):
    stat = os.stat(file_path)
    atime = stat.st_atime
    mtime = new_datetime.timestamp()
    os.utime(file_path, times=(atime, mtime))


def test_default_watchments_attachments(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    watched_attachments = hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == []


def test_add_empty_list(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_calculator.addWatchAttachments(wikipage, [])
    watched_attachments = hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == []


def test_add_single_file(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_calculator.addWatchAttachments(wikipage, ["image.png"])
    watched_attachments = hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == ["image.png"]


def test_add_two_files(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_calculator.addWatchAttachments(wikipage, ["image.png", "dirname/file.txt"])
    watched_attachments = hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == ["image.png", "dirname/file.txt"]


def test_add_two_files_two_steps(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_calculator.addWatchAttachments(wikipage, ["image.png"])
    hash_calculator.addWatchAttachments(wikipage, ["dirname/file.txt"])
    watched_attachments = hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == ["image.png", "dirname/file.txt"]


def test_add_two_files_separate_calculators(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_calculator.addWatchAttachments(wikipage, ["image.png", "dirname/file.txt"])

    new_hash_calculator = SimpleHashCalculator(application)
    watched_attachments = new_hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == ["image.png", "dirname/file.txt"]


def test_add_two_files_many_calculators(application: Application, wikipage: WikiPage):
    first_hash_calculator = SimpleHashCalculator(application)
    first_hash_calculator.addWatchAttachments(wikipage, ["image.png"])

    second_hash_calculator = SimpleHashCalculator(application)
    second_hash_calculator.addWatchAttachments(wikipage, ["dirname/file.txt"])

    new_hash_calculator = SimpleHashCalculator(application)
    watched_attachments = new_hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == ["image.png", "dirname/file.txt"]


def test_clear(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_calculator.addWatchAttachments(wikipage, ["image.png"])
    hash_calculator.addWatchAttachments(wikipage, ["dirname/file.txt"])
    hash_calculator.clearWatchAttachments(wikipage)
    watched_attachments = hash_calculator.getWatchAttachments(wikipage)
    assert watched_attachments == []


def test_files_dont_exist(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)

    hash_1 = hash_calculator.getHash(wikipage)
    
    hash_calculator.addWatchAttachments(wikipage, ["image.png"])
    hash_2 = hash_calculator.getHash(wikipage)

    hash_calculator.addWatchAttachments(wikipage, ["dirname/file.txt"])
    hash_3 = hash_calculator.getHash(wikipage)

    assert hash_1 != hash_2
    assert hash_1 != hash_3
    assert hash_2 != hash_3


def test_attachments_dont_watch(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    hash_1 = hash_calculator.getHash(wikipage)

    hash_calculator.addWatchAttachments(wikipage, ["image.png"])
    hash_2 = hash_calculator.getHash(wikipage)

    copy_test_files_to_attachments(wikipage, ["image.png"])
    hash_3 = hash_calculator.getHash(wikipage)

    assert hash_1 != hash_2
    assert hash_1 != hash_3
    assert hash_2 != hash_3


def test_change_attach_datetime(application: Application, wikipage: WikiPage):
    hash_calculator = SimpleHashCalculator(application)
    attach_files = copy_test_files_to_attachments(wikipage, ["image.png"])
    hash_calculator.addWatchAttachments(wikipage, ["image.png"])
    hash_1 = hash_calculator.getHash(wikipage)

    set_file_times(attach_files[0], datetime.datetime(2026, 7, 11))
    hash_2 = hash_calculator.getHash(wikipage)

    assert hash_1 != hash_2
