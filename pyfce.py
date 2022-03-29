from argparse import ArgumentParser
from sys import argv, exit

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def do_auth():
    user = input('type the user: ')
    passwd = input('type the password: ')

    ret = auth(user, passwd)

    if ret:
        print('the credentials are valid')
    else:
        print('failed to login with the provided credentials')

def auth(user, passwd):
    op = ChromeOptions()
    op.add_argument('headless')

    drv = Chrome(options=op)

    drv.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=1001')
    drv.find_element(by=By.XPATH, value='//*[@id="txtLogin"]').send_keys(user)
    drv.find_element(by=By.XPATH, value='//*[@id="txtSenha"]').send_keys(passwd)
    drv.find_element(by=By.XPATH, value='//*[@id="btnOk"]').click()

    try:
        drv.find_element(by=By.XPATH, value='//*[@id="Image1"]')

        return True
    except NoSuchElementException:
        return False

def parse_args():
    parser = ArgumentParser(prog='pyfce')

    parser.add_argument(
        '-c',
        '--check-credentials',
        help='check the provided credentials',
        action='store_true'
    )

    # no arguments were provided
    if len(argv) == 1:
        parser.print_help()

    return parser.parse_args()

def main(args):
    if args.check_credentials:
        do_auth()

if __name__ == "__main__":
    try:
        args = parse_args()

        main(args)
    except Exception as err:
        print(err)
        exit(1)
