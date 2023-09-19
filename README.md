# Folder Synchronization Tool

## Overview

This is a Python-based command-line tool for synchronizing two folders: a source folder and a replica folder. The tool ensures that the replica folder maintains an identical copy of the source folder. Synchronization is performed periodically, and all file creation, copying, and removal operations are logged to both a log file and the console output.

## Features

- **One-way synchronization:** Syncs content from the source folder to the replica folder.
- **Periodic synchronization:** Configurable time interval for synchronization.
- **Logging:** Detailed logging of synchronization operations.
- **Command-line interface:** Easy-to-use command-line arguments for configuration.

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. **Clone this repository** to your local machine:
`git@github.com:moeezaziz/Syncr.git`

2. **Navigate to the project directory**:
`cd syncr`

3. **Install the required dependencies** (if not already installed):
`pip install -r requirements.txt`

## Usage

### Command-Line Arguments

- `--source`: The source folder to sync from.
- `--destination`: The replica folder to sync to.
- `--log`: The log file to record synchronization operations.
- `--interval`: The synchronization interval in seconds.

### Example Usage
`python sync_directories.py --source /path/to/source/folder --destination /path/to/replica/folder --log sync.log --interval 3600`

This example synchronizes the source folder to the replica folder every 3600 seconds (1 hour) and logs operations to `sync.log`.

You can also directly run `python sync_directories.py`and enter the arguments using the command line interface.
### Running Tests

You can run the included unit tests to ensure the tool's functionality:
`test_sync_directories.py`

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the repository**.
2. Create a new branch for your feature or bug fix.
3. **Make your changes** and commit them with clear messages.
4. **Push your changes** to your fork.
5. **Submit a pull request** to the main repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This tool was developed as a solution to a synchronization task and makes use of Python libraries such as `os`, `time`, `filecmp`, and `shutil`. Additionally, it uses the `click` library for command-line argument parsing.

## Contact

If you have any questions or suggestions, feel free to contact me at moeezazizch@gmail.com
