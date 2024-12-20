import sys


class Builtins:
    def _exit(args):
        exit()

    def _echo(args):
        print(' '.join(args[1:]))

    def _type(args):
        command = args[1]
        if command in Builtins.builtins:
            print(f"{command} is a shell builtin")
        else:
            print(f"{command}: not found")

    builtins = {
        'exit': _exit,
        'echo': _echo,
        'type': _type,
    }


def handle_not_found(args):
    command = args[0]
    print(f"{command}: command not found")


def main():
    while True:
        sys.stdout.write("$ ")

        user_input = input()
        args = user_input.split()
        command = args[0]

        program = Builtins.builtins.get(command, handle_not_found)
        program(args)


if __name__ == "__main__":
    main()
