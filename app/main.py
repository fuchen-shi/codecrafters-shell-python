import sys


def main():
    sys.stdout.write("$ ")

    # Wait for user input
    user_input = input()

    print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
