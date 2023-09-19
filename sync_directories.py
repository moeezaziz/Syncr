import os
import sys
import time
import filecmp
import shutil
import click


class FolderSynchronizer:
    def __init__(self, source, destination, log, interval):
        self.source_dir = source
        self.replica_dir = destination
        self.log_file = log
        self.interval = interval

    def synchronize(self):
        try:
            click.echo("---------Comparing source and destination-----------")
            dcmp = filecmp.dircmp(self.source_dir, self.replica_dir)
            if not dcmp.diff_files:
                click.echo("No changes detected!")
            self._copy_new_files(dcmp.left_only)
            self._remove_extra_files(dcmp.right_only)
            self._update_changed_files(dcmp.diff_files)
        except Exception as e:
            self._log(f"Error: {str(e)}")

    def _copy_new_files(self, files):
        for name in files:
            src_path = os.path.join(self.source_dir, name)
            dst_path = os.path.join(self.replica_dir, name)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                self._log(f"File copied: {src_path} -> {dst_path}")
            else:
                shutil.copytree(src_path, dst_path, False, None)
                self._log(f"Folder copied: {src_path} -> {dst_path}")

    def _remove_extra_files(self, files):
        for name in files:
            path = os.path.join(self.replica_dir, name)
            if os.path.isfile(path):
                os.remove(path)
                self._log(f"File removed: {path}")
            else:
                shutil.rmtree(path)
                self._log(f"Folder removed: {path}")

    def _update_changed_files(self, files):
        for name in files:
            src_path = os.path.join(self.source_dir, name)
            dst_path = os.path.join(self.replica_dir, name)
            shutil.copy2(src_path, dst_path)
            self._log(f"File updated: {src_path} -> {dst_path}")

    def _log(self, message):
        with open(self.log_file, "a") as log:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] {message}\n")
            print(message)


@click.command()
@click.option('--source', required=True, prompt='Source folder')
@click.option('--destination', required=True, prompt='Destination folder')
@click.option('--log', required=True, prompt='Log file')
@click.option('--interval', required=True, prompt='Sync interval', type=int)
def main(source, destination, log, interval):
    synchronizer = FolderSynchronizer(source, destination, log, interval)
    while True:
        synchronizer.synchronize()
        time.sleep(synchronizer.interval)  # Synchronize every hour (3600 seconds)


if __name__ == "__main__":

    main()
