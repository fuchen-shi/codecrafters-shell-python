import sys


def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        command_list = command.split()
        program = command_list[0]
        args = command_list[1:]

        match program:
            case 'exit':
                return
            case 'echo':
                print(' '.join(args))
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
