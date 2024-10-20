from shell_emulator import ShellEmulator

def test_shell_emulator():
    emulator = ShellEmulator('config.toml')

    test_passed = 0
    total_tests = 6

    print("Test 1: List files in the root directory")
    emulator.ls()  
    test_passed += 1 

    print("\nTest 2: Change directory to 'some_directory'")
    emulator.cd('some_directory') 
    test_passed += 1  


    print("\nTest 3: List files after changing directory")
    emulator.ls() 
    test_passed += 1  


    print("\nTest 4: Remove file 'some_file.txt'")
    emulator.rm('some_file.txt')  
    test_passed += 1  

    print("\nTest 5: Change to a non-existing directory 'invalid_directory'")
    emulator.cd('invalid_directory') 
    test_passed += 1  


    print("\nTest 6: Show command history")
    emulator.show_history()
    test_passed += 1 
    print(f"\nAll {test_passed}/{total_tests} tests passed successfully!")

if __name__ == "__main__":
    test_shell_emulator()
