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
            print(f'{command} is a shell builtin')
            return

        command_path = get_command_path(command)
        if command_path:
            print(f'{command} is {command_path}')
            return

        print(f'{command}: not found')

    def _pwd(args):
        path_list = Cwd.get()
        path_str = Cwd.list_to_str(path_list)
        print(path_str)

    def _cd(args):
        HOME = os.environ['HOME']
        input_path = args[1]

        if input_path[0] == '~':
            input_path = f'{HOME}{input_path[1:]}'

        if input_path == '/':
            Cwd.set([])
            return

        path_list = []

        if input_path[0] != '/':  # Relative path
            path_list = Cwd.get()

        steps = input_path.strip('/').split('/')

        for step in steps:
            match step:
                case '.':
                    pass
                case '..':
                    path_list = path_list[:-1]
                case _:
                    path_list.append(step)

        path_str = Cwd.list_to_str(path_list)

        if os.path.isdir(path_str):
            Cwd.set(path_list)
            return

        print(f'cd: {input_path}: No such file or directory')

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
    _path_list = []

    def get():
        return Cwd._path_list.copy()

    def set(path_list):
        Cwd._path_list = path_list

    def str_to_list(path_str):
        if path_str == '/':
            return []

        return path_str.strip('/').split('/')

    def list_to_str(path_list):
        return f'/{'/'.join(path_list)}'

    def init():
        path_str = os.getcwd()
        path_list = Cwd.str_to_list(path_str)
        Cwd.set(path_list)


def init():
    Cwd.init()


def parse_input(user_input):
    args = []
    current_arg = None

    is_escaping = False
    is_inside_single_quotes = False
    is_inside_double_quotes = False

    for c in user_input + ' ':
        if is_escaping:  # Escape current
            current_arg = current_arg or ''
            current_arg += c
            is_escaping = False
            continue

        if c == '\\' and not is_inside_single_quotes:  # Escape next
            is_escaping = True
            continue

        if c == '\'' and not is_inside_double_quotes:  # Toggle single quote
            current_arg = current_arg or ''
            is_inside_single_quotes = not is_inside_single_quotes
            continue

        if c == '"' and not is_inside_single_quotes:  # Toggle double quote
            current_arg = current_arg or ''
            is_inside_double_quotes = not is_inside_double_quotes
            continue

        if c != ' ' or (c == ' ' and (is_inside_single_quotes or is_inside_double_quotes)):  # Ordinary char
            current_arg = current_arg or ''
            current_arg += c
            continue

        if current_arg is not None:  # Split args
            args.append(current_arg)
            current_arg = None

    return args


def rep():
    sys.stdout.write('$ ')

    user_input = input()
    args = parse_input(user_input)

    run_program(args)


def get_command_path(command):
    PATH = os.environ['PATH']
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

    print(f'{command}: command not found')


def main():
    init()

    while True:
        rep()


if __name__ == '__main__':
    main()
