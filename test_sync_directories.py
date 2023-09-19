#!/usr/bin/env python3

import os
import shutil
import time
import pytest
from pathlib import Path
from sync_directories import FolderSynchronizer


@pytest.fixture(scope="function")
def setup_folders(tmp_path: Path) -> tuple:
    """
    Fixture to set up temporary source, destination, and log folders for testing.

    Returns:
        tuple: A tuple containing source directory, destination directory, and log file Path.
    """
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    destination_dir = tmp_path / "destination"
    destination_dir.mkdir()
    log_file = tmp_path / "log.txt"

    yield source_dir, destination_dir, log_file


def test_copy_new_files(setup_folders: tuple) -> None:
    """
    Test copying new files from source to destination.

    Args:
        setup_folders (tuple): A tuple containing source directory, destination directory, and log file Path.
    """
    source_dir, destination_dir, log_file = setup_folders
    synchronizer = FolderSynchronizer(source_dir, destination_dir, log_file, 1)

    new_file_path = source_dir / "new_file.txt"
    new_file_path.write_text("Test content")

    synchronizer.synchronize()

    assert (destination_dir / "new_file.txt").exists()


def test_remove_extra_files(setup_folders: tuple) -> None:
    """
    Test removing extra files from the destination directory.

    Args:
        setup_folders (tuple): A tuple containing source directory, destination directory, and log file Path.
    """
    source_dir, destination_dir, log_file = setup_folders
    synchronizer = FolderSynchronizer(source_dir, destination_dir, log_file, 1)

    extra_file_path = destination_dir / "extra_file.txt"
    extra_file_path.write_text("Test content")

    synchronizer.synchronize()

    assert not extra_file_path.exists()


def test_update_changed_files(setup_folders: tuple) -> None:
    """
    Test updating changed files in the destination directory with source versions.

    Args:
        setup_folders (tuple): A tuple containing source directory, destination directory, and log file Path.
    """
    source_dir, destination_dir, log_file = setup_folders
    synchronizer = FolderSynchronizer(source_dir, destination_dir, log_file, 1)

    source_file_path = source_dir / "changed_file.txt"
    source_file_path.write_text("Source content")
    destination_file_path = destination_dir / "changed_file.txt"
    destination_file_path.write_text("Destination content")

    synchronizer.synchronize()

    with open(destination_file_path) as f:
        content = f.read()
    assert content == "Source content"


if __name__ == "__main__":
    pytest.main()
