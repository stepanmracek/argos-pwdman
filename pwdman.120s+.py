#!/usr/bin/env python3
from collections import namedtuple, defaultdict
from os import path

ENCRYPTED_DIR = "/home/user/.encrypted/"
DECRYPTED_DIR = "/home/user/.decrypted/"
PASSWORD_FILE = "pwd"
MAX_ITEMS_IN_GROUP = 20

Account = namedtuple('Account', ['service', 'username', 'password'])


def header():
    print("|iconName=dialog-password-symbolic ")
    print("---")


def mount_command():
    print(
        "Mount EncFS | terminal='false' bash='python ~/.config/argos/pwdman.mount.py {} {}'"
        .format(ENCRYPTED_DIR, DECRYPTED_DIR)
    )


def unmount_command():
    print("Unmount EncFS | terminal='false' bash='encfs -u {}'".format(DECRYPTED_DIR))


def is_mounted():
    return path.exists(DECRYPTED_DIR + PASSWORD_FILE)


def get_accounts():
    with open(DECRYPTED_DIR + PASSWORD_FILE) as f:
        lines = (line.split() for line in f.readlines() if len(line.split()) >= 3)
    return (Account(service=line[0], username=line[1], password=line[2]) for line in lines)


def get_accounts_per_letter(accounts):
    accounts_per_letter = defaultdict(list)
    for account in accounts:
        accounts_per_letter[account.service[0].upper()].append(account)
    return accounts_per_letter


def get_accounts_in_groups(accounts_per_letter):
    accounts_in_groups = []
    current_group = []
    accounts_in_groups.append(current_group)
    for letter in sorted(accounts_per_letter.keys()):
        if len(current_group) > 0 and len(current_group) + len(accounts_per_letter[letter]) > MAX_ITEMS_IN_GROUP:
            current_group = []
            accounts_in_groups.append(current_group)
        current_group += sorted(accounts_per_letter[letter], key=lambda account: account.service)
    return accounts_in_groups


def account_to_menu_item(account):
    return (
        "{}: {} | terminal='false' bash='echo -n {} | xclip -selection c'"
        .format(account.service, account.username, account.password)
    )


def print_accounts(accounts_in_groups):
    if len(accounts_in_groups) > 1:
        for group in accounts_in_groups:
            if len(group) > 0 and group[0].service[0] != group[-1].service[0]:
                print("{} - {}".format(group[0].service[0].upper(), group[-1].service[0].upper()))
            else:
                print(group[0].service[0].upper())
            for account in group:
                print("--{}".format(account_to_menu_item(account)))
    else:
        for account in accounts_in_groups[0]:
            print("{}".format(account_to_menu_item(account)))


def main():
    header()

    if not is_mounted():
        mount_command()
    else:
        unmount_command()
        accounts = get_accounts()
        accounts_per_letter = get_accounts_per_letter(accounts)
        accounts_in_groups = get_accounts_in_groups(accounts_per_letter)
        print_accounts(accounts_in_groups)


if __name__ == '__main__':
    main()
