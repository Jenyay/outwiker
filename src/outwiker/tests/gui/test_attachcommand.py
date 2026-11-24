# -*- coding: utf-8 -*-

from pathlib import Path

from outwiker.api.app.attachment import attachFiles
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiPage
from outwiker.gui.tester import Tester, getButtonId
from outwiker.utilites.textfile import readTextFile


def _get_files_path(samplefiles_path: Path, files: list[str]) -> list[Path]:
    return [samplefiles_path / fname for fname in files]


def _create_attach_subdir(page: WikiPage, subdir: str) -> Path:
    return Attachment(page).createSubdir(subdir)


def test_attach_simple(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    files = ["image.png", "add.png"]
    files_full_path = _get_files_path(samplefiles_path, files)
    attachFiles(main_window, selected_page, files_full_path)

    attach = Attachment(selected_page)
    assert len(files) == len(attach.getAttachFull())


def test_attach_self(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    files = ["image.png", "add.png"]
    files_full_path = _get_files_path(samplefiles_path, files)
    attachFiles(main_window, selected_page, files_full_path)

    attach = Attachment(selected_page)
    attachFiles(main_window, selected_page, attach.getAttachFull())

    assert len(files) == len(attach.getAttachFull())


def test_attach_self_in_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    fname = "image.png"
    subdir = "subdir"
    _create_attach_subdir(selected_page, subdir)

    file_full_path = _get_files_path(samplefiles_path, [fname])
    attachFiles(main_window, selected_page, file_full_path, subdir)

    attach = Attachment(selected_page)
    file_new_path = Path(attach.getAttachPath(subdir), fname)
    attachFiles(main_window, selected_page, [file_new_path])

    assert len(attach.getAttachFull(subdir)) == 1


def test_add_attaches(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    files_full_path_1 = _get_files_path(samplefiles_path, ["image.png", "add.png"])
    files_full_path_2 = _get_files_path(samplefiles_path, ["accept.png"])
    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    assert len(files_full_path_1) + len(files_full_path_2) == len(
        attach.getAttachFull()
    )


def test_attach_dir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    files_full_path = _get_files_path(samplefiles_path, ["dir"])
    attachFiles(main_window, selected_page, files_full_path)

    attach = Attachment(selected_page)
    assert len(files_full_path) == len(attach.getAttachFull())

    attach_dir = Path(attach.getAttachPath())
    assert (attach_dir / "dir").is_dir()
    assert (attach_dir / "dir" / "attach.png").exists()
    assert (attach_dir / "dir" / "subdir").is_dir()
    assert (attach_dir / "dir" / "subdir" / "subdir2").is_dir()
    assert (attach_dir / "dir" / "subdir" / "subdir2" / "image.png").exists()


def test_attach_subdir_root(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    files = ["image.png", "add.png"]
    files_full_path = _get_files_path(samplefiles_path, files)
    subdir = "."
    attachFiles(main_window, selected_page, files_full_path, subdir)

    attach = Attachment(selected_page)
    assert len(files) == len(attach.getAttachFull())


def test_attach_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    subdir = "dir"
    subdir_full = _create_attach_subdir(selected_page, subdir)

    files_full_path = _get_files_path(samplefiles_path, ["image.png", "add.png"])
    attachFiles(main_window, selected_page, files_full_path, subdir)

    assert (subdir_full / "image.png").exists()
    assert (subdir_full / "add.png").exists()


def test_attach_dir_to_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    subdir = "dir"

    # Create __attach directory
    attach = Attachment(selected_page)
    attach_dir = Path(attach.getAttachPath(create=True))
    _create_attach_subdir(selected_page, subdir)

    files_full_path = _get_files_path(samplefiles_path, [Path("dir", "subdir")])
    attachFiles(main_window, selected_page, files_full_path, subdir)

    assert (attach_dir / "dir" / "subdir").is_dir()
    assert (attach_dir / "dir" / "subdir" / "subdir2").is_dir()
    assert (attach_dir / "dir" / "subdir" / "subdir2" / "image.png").exists()


def test_overwrite_dialog_overwrite(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    Tester.dialogTester.append(getButtonId, "overwrite")

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"]
    )

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 2" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_overwrite_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    subdir = "dir"
    Tester.dialogTester.append(getButtonId, "overwrite")
    _create_attach_subdir(selected_page, subdir)

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"]
    )

    attachFiles(main_window, selected_page, files_full_path_1, subdir)
    attachFiles(main_window, selected_page, files_full_path_2, subdir)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), subdir, "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 2" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_overwrite_skip(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    Tester.dialogTester.append(getButtonId, "skip")

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"]
    )

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 1" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_overwrite_many(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    count = 5

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"] * count
    )

    for n in range(count):
        Tester.dialogTester.append(getButtonId, "overwrite")

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 2" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_overwrite_all(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    count = 5

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"] * count
    )

    Tester.dialogTester.append(getButtonId, "overwriteAll")

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 2" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_skip_many(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    count = 5

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"] * count
    )

    for n in range(count):
        Tester.dialogTester.append(getButtonId, "skip")

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 1" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_skip_all(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    count = 5

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"] * count
    )

    Tester.dialogTester.append(getButtonId, "skipAll")

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 1" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_overwrite_in_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    Tester.dialogTester.append(getButtonId, "overwrite")
    subdir = "subdir"

    _create_attach_subdir(selected_page, subdir)

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"]
    )

    attachFiles(main_window, selected_page, files_full_path_1, subdir)
    attachFiles(main_window, selected_page, files_full_path_2, subdir)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), subdir, "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 2" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_skip_in_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    Tester.dialogTester.append(getButtonId, "skip")
    subdir = "subdir"

    _create_attach_subdir(selected_page, subdir)

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"]
    )

    attachFiles(main_window, selected_page, files_full_path_1, subdir)
    attachFiles(main_window, selected_page, files_full_path_2, subdir)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), subdir, "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 1" in text
    assert Tester.dialogTester.count == 0


def test_write_to_existing_subdir(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    subdir = "subdir2"
    files_full_path = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/subdir1/subdir2"]
    )

    _create_attach_subdir(selected_page, subdir)

    attachFiles(main_window, selected_page, files_full_path)

    attach = Attachment(selected_page)
    assert len(attach.getAttachFull(subdir)) == 2


def test_overwrite_dialog_cancel_single(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    Tester.dialogTester.appendCancel()

    files_full_path_1 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_1/file_1.txt"]
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path, ["for_overwrite/version_2/file_1.txt"]
    )

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 1" in text
    assert Tester.dialogTester.count == 0


def test_overwrite_dialog_overwrite_and_cancel(
    main_window: MainWindow, selected_page: WikiPage, samplefiles_path: Path
):
    Tester.dialogTester.append(getButtonId, "overwrite")
    Tester.dialogTester.appendCancel()

    files_full_path_1 = _get_files_path(
        samplefiles_path,
        ["for_overwrite/version_1/file_1.txt", "for_overwrite/version_1/file_2.txt"],
    )
    files_full_path_2 = _get_files_path(
        samplefiles_path,
        ["for_overwrite/version_2/file_1.txt", "for_overwrite/version_2/file_2.txt"],
    )

    attachFiles(main_window, selected_page, files_full_path_1)
    attachFiles(main_window, selected_page, files_full_path_2)

    attach = Attachment(selected_page)
    attach_fname = Path(attach.getAttachPath(), "file_1.txt")

    text = readTextFile(attach_fname)
    assert "version 1" in text
    assert Tester.dialogTester.count == 0
