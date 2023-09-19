#!/usr/bin/env python3

import os
import time
import filecmp
import shutil
import click
from pathlib import Path


class FolderSynchronizer:
    def __init__(self, source: Path, destination: Path, log: Path, interval: int) -> None:
        """Initializes the FolderSynchronizer with source and destination directories,
        and a log file.

        :param source: The source directory to sync from.
        :param destination: The replica directory to sync to.
        :param log: The log file to record synchronization operations.
        :param interval: The time interval between each sync in seconds.
        """
        self.source_dir = Path(source)
        self.destination_dir = Path(destination)
        self.log_file = Path(log)
        self.interval = interval

    def synchronize(self) -> None:
        """
        Synchronizes the source directory with the destination directory.
        """
        try:
            click.echo("---------Comparing source and destination-----------")
            if not os.path.isdir(self.destination_dir):
                click.echo("Directory does not exist! Creating a new one...")
                os.mkdir(self.destination_dir)
                self._log(f"Directory created at {self.destination_dir}")
            dcmp = filecmp.dircmp(self.source_dir, self.destination_dir)
            click.echo(dcmp.report())
            self._copy_new_files(dcmp.left_only)
            self._remove_extra_files(dcmp.right_only)
            self._update_changed_files(dcmp.diff_files)
        except Exception as e:
            self._log(f"Error: {str(e)}")
        click.echo("--------------Comparison complete----------------------")

    def _copy_new_files(self, files: list) -> None:
        """
        Copies new files or folders from the source to the destination directory.

        :param files: List of new files or folders.
        """
        for name in files:
            src_path = self.source_dir / name
            dst_path = self.destination_dir / name
            if not dst_path.exists():
                if src_path.is_file():
                    shutil.copy2(src_path, dst_path)
                    self._log(f"File copied: {src_path} -> {dst_path}")
                else:
                    shutil.copytree(src_path, dst_path, False, None)
                    self._log(f"Folder copied: {src_path} -> {dst_path}")

    def _remove_extra_files(self, files: list) -> None:
        """
        Removes extra files or folders from the destination directory.

        :param files: List of extra files or folders.
        """
        for name in files:
            path = self.destination_dir / name
            if path.exists():
                if path.is_file():
                    path.unlink()
                    self._log(f"File removed: {path}")
                else:
                    shutil.rmtree(path)
                    self._log(f"Folder removed: {path}")

    def _update_changed_files(self, files: list) -> None:
        """
        Updates changed files in the destination directory with source versions.

        :param files: List of changed files.
        """
        for name in files:
            src_path = self.source_dir / name
            dst_path = self.destination_dir / name
            if dst_path.exists():
                shutil.copy2(src_path, dst_path)
                self._log(f"File updated: {src_path} -> {dst_path}")

    def _log(self, message: str) -> None:
        """
        Logs a message to the specified log file and prints it to the console.

        :param message: The message to log.
        """
        with open(self.log_file, "a") as log:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] {message}\n")
            print(message)


@click.command()
@click.option('--source', required=True, type=click.Path(exists=True, file_okay=False, dir_okay=True),
              prompt='Source folder', help='Source folder')
@click.option('--destination', required=True, type=click.Path(file_okay=False, dir_okay=True),
              prompt='Destination folder', help='Destination folder')
@click.option('--log', required=True, type=click.Path(writable=True),
              prompt='Log file', help='Log file')
@click.option('--interval', required=True, type=int, prompt='Sync interval in seconds',
              help='Sync interval in seconds')
def main(source: Path, destination: Path, log: Path, interval: int) -> None:
    synchronizer = FolderSynchronizer(source, destination, log, interval)
    while True:
        synchronizer.synchronize()
        time.sleep(synchronizer.interval)


if __name__ == "__main__":

    main()
