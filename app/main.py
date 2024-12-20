import sys
import os
import subprocess
from pathlib import PurePath


class Builtins:
    def _exit(args):
        exit()

    def _echo(args):
        print(' '.join(args[1:]))

    def _type(args):
        command = args[1]

        builtin = Builtins.get(command)
        if builtin:
            print(f"{command} is a shell builtin")
            return

        command_path = get_command_path(command)
        if command_path:
            print(f"{command} is {command_path}")
            return

        print(f"{command}: not found")

    def _pwd(args):
        cwd = Cwd.get()
        print(cwd)

    def _cd(args):
        new_dir = args[1]

        if os.path.isdir(new_dir):
            Cwd.set(new_dir)
            return

        print(f"cd: {new_dir}: No such file or directory")

    _builtins = {
        'exit': _exit,
        'echo': _echo,
        'type': _type,
        'pwd': _pwd,
        'cd': _cd
    }

    def get(command):
        return Builtins._builtins.get(command)


class Cwd:
    _cwd = None

    def init():
        Cwd._cwd = os.getcwd()

    def get():
        return Cwd._cwd

    def set(new_dir):
        Cwd._cwd = new_dir


def init():
    Cwd.init()


def rep():
    sys.stdout.write("$ ")

    user_input = input()
    args = user_input.split()

    run_program(args)


def get_command_path(command):
    PATH = os.environ["PATH"]
    path_list = PATH.split(':')

    for path in path_list:
        command_path = PurePath(path, command).as_posix()
        if os.path.isfile(command_path):
            return command_path

    return None


def run_program(args):
    command = args[0]

    builtin = Builtins.get(command)
    if builtin:
        builtin(args)
        return

    command_path = get_command_path(command)
    if command_path:
        subprocess.run([command_path] + args[1:])
        return

    print(f"{command}: command not found")


def main():
    init()

    while True:
        rep()


if __name__ == "__main__":
    main()
