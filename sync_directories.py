import os
import sys
import time
import filecmp
import shutil


def synchronize_folders(source_dir, replica_dir, log_file):
    try:
        compare = filecmp.dircmp(source_dir, replica_dir)
        for name in compare.left_only:
            src_path = os.path.join(source_dir, name)
            dst_path = os.path.join(replica_dir, name)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                log(log_file, f"File copied: {src_path} -> {dst_path}")
            else:
                shutil.copytree(src_path, dst_path, False, None)
                log(log_file, f"Folder copied: {src_path} -> {dst_path}")

        for name in compare.right_only:
            path = os.path.join(replica_dir, name)
            if os.path.isfile(path):
                os.remove(path)
                log(log_file, f"File removed: {path}")
            else:
                shutil.rmtree(path)
                log(log_file, f"Folder removed: {path}")

        for name in compare.diff_files:
            src_path = os.path.join(source_dir, name)
            dst_path = os.path.join(replica_dir, name)
            shutil.copy2(src_path, dst_path)
            log(log_file, f"File updated: {src_path} -> {dst_path}")

    except Exception as e:
        log(log_file, f"Error: {str(e)}")


def log(log_file, message):
    with open(log_file, "a") as log:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")
        print(message)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sync_directories.py source_folder replica_folder log_file")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    log_file = sys.argv[3]

    while True:
        synchronize_folders(source_folder, replica_folder, log_file)
        time.sleep(3600)  # Synchronize every hour (3600 seconds)
