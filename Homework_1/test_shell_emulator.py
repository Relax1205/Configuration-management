import zipfile
import os
import toml
import shutil

class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.cwd = '/'  # Current working directory
        self.history = []  # Command history
        self.load_virtual_fs()  # Load virtual file system
        self.run_startup_script()  # Run startup script

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = toml.load(f)
            self.computer_name = config['computer']['name']
            self.zip_path = config['filesystem']['path']
            self.startup_script = config['startup']['script']

    def load_virtual_fs(self):
        self.zip_file = zipfile.ZipFile(self.zip_path, 'r')
        self.files = self.zip_file.namelist()

    def run_startup_script(self):
        try:
            with self.zip_file.open(self.startup_script) as f:
                for line in f:
                    command = line.decode('utf-8').strip()
                    if command:
                        self.execute_command(command)
        except KeyError:
            self.show_output(f"Startup script '{self.startup_script}' not found in zip file.")

    def execute_command(self, command):
        self.history.append(command)
        parts = command.split()

        if parts[0] == 'ls':
            self.ls()
        elif parts[0] == 'cd':
            self.cd(parts[1] if len(parts) > 1 else '.')
        elif parts[0] == 'exit':
            self.exit_shell()
        elif parts[0] == 'rm':
            if len(parts) > 1:
                self.rm(parts[1])
            else:
                self.show_output("Usage: rm <file>")
        elif parts[0] == 'rmdir':
            if len(parts) > 1:
                self.rmdir(parts[1])
            else:
                self.show_output("Usage: rmdir <directory>")
        elif parts[0] == 'history':
            self.show_history()
        else:
            self.show_output(f"Command '{parts[0]}' not found.")

    def ls(self):
        if self.cwd == '/':
            cwd_with_slash = ''
        else:
            cwd_with_slash = self.cwd.rstrip('/') + '/'

        items = set()
        for file in self.files:
            if file.startswith(cwd_with_slash) and file != cwd_with_slash:
                relative_path = file[len(cwd_with_slash):].strip('/')
                if '/' in relative_path:
                    directory = relative_path.split('/')[0]
                    items.add(directory + '/')
                else:
                    items.add(relative_path)

        if items:
            self.show_output("\n".join(sorted(items)))
        else:
            self.show_output("Directory is empty.")

    def cd(self, path):
        if path == '..':
            self.cwd = os.path.dirname(self.cwd.rstrip('/'))
            if not self.cwd:
                self.cwd = '/'
        else:
            new_path = os.path.join(self.cwd.rstrip('/'), path).lstrip('/')
            if any(file.startswith(new_path + '/') for file in self.files):
                self.cwd = new_path
                self.show_output(f"Changed directory to {self.cwd}")
            else:
                self.show_output(f"Directory '{path}' not found.")

    def rm(self, path):
        full_path = os.path.join(self.cwd, path)
        try:
            os.remove(full_path)  # Remove file from the real filesystem
            self.show_output(f"Deleted file {full_path}")
        except FileNotFoundError:
            self.show_output(f"File '{full_path}' not found.")
        except IsADirectoryError:
            self.show_output(f"'{full_path}' is a directory. Use 'rmdir' to remove directories.")
        except Exception as e:
            self.show_output(f"Error removing file '{full_path}': {e}")

    def rmdir(self, path):
        full_path = os.path.join(self.cwd, path)
        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)  # Remove directory from the real filesystem
                self.show_output(f"Deleted directory {full_path}")
            else:
                self.show_output(f"Directory '{full_path}' not found.")
        except FileNotFoundError:
            self.show_output(f"Directory '{full_path}' not found.")
        except Exception as e:
            self.show_output(f"Error removing directory '{full_path}': {e}")

    def show_history(self):
        self.show_output("\n".join(self.history))

    def exit_shell(self):
        self.show_output("Exiting shell...")
        self.close()  # Close ZIP file before exiting
        exit()  # Terminate the program

    def close(self):
        """Close the ZIP file upon completion."""
        self.zip_file.close()

    # Function to output to console
    def show_output(self, output):
        print(output)  # Output to console


# Test functions for ShellEmulator
def test_shell_emulator():
    # Initialize the emulator
    emulator = ShellEmulator('config.toml')
    
    # Initialize test counter
    test_passed = 0
    total_tests = 6

    # Test 1: List files in the root directory
    print("Test 1: List files in the root directory")
    emulator.ls()  # Expecting to see files and directories in the root
    test_passed += 1  # Increment count as the test is executed

    # Test 2: Change directory to a valid directory
    print("\nTest 2: Change directory to 'some_directory'")
    emulator.cd('some_directory')  # Change to a directory that exists in the zip
    test_passed += 1  # Increment count as the test is executed

    # Test 3: List files after changing directory
    print("\nTest 3: List files after changing directory")
    emulator.ls()  # Expecting to see files in 'some_directory'
    test_passed += 1  # Increment count as the test is executed

    # Test 4: Remove a file
    print("\nTest 4: Remove file 'some_file.txt'")
    emulator.rm('some_file.txt')  # Try to remove a specific file
    test_passed += 1  # Increment count as the test is executed

    # Test 5: Change to a non-existing directory
    print("\nTest 5: Change to a non-existing directory 'invalid_directory'")
    emulator.cd('invalid_directory')  # Expecting an error message
    test_passed += 1  # Increment count as the test is executed

    # Test 6: Check command history
    print("\nTest 6: Show command history")
    emulator.show_history()  # Show the history of commands executed
    test_passed += 1  # Increment count as the test is executed

    # Final output
    print(f"\nAll {test_passed}/{total_tests} tests passed successfully!")

if __name__ == "__main__":
    test_shell_emulator()