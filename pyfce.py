from argparse import ArgumentParser
from getpass import getpass
from sys import argv, exit

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def do_auth(drv):
    user = input('user: ')
    passwd = getpass('password: ')

    if auth(drv, user, passwd):
        print('the credentials are valid')
    else:
        print('the credentials are invalid')

def auth(drv, user, passwd):
    drv.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=1001')

    drv.find_element(by=By.XPATH, value='//*[@id="txtLogin"]').send_keys(user)
    drv.find_element(by=By.XPATH, value='//*[@id="txtSenha"]').send_keys(passwd)
    drv.find_element(by=By.XPATH, value='//*[@id="btnOk"]').click()

    # check the authentication result by finding the 'exit' button
    try:
        drv.find_element(by=By.XPATH, value='//*[@id="Image1"]')

        return True
    except NoSuchElementException:
        return False

def do_is_matriculation_available(drv):
    user = input('user: ')
    passwd = getpass('password: ')

    if auth(drv, user, passwd):
        if is_matriculation_available(drv):
            print('matriculation available')
        else:
            print('matriculation not available')

def is_matriculation_available(drv):
    txt = '- Não há nenhuma etapa de pedido de matrícula aberta no momento.'

    drv.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2047')

    try:
        element = drv.find_element(
            by=By.XPATH,
            value='/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]'
                + '/table[2]/tbody/tr/td[2]/span'
        )

        if element.text == txt:
            return False
    except NoSuchElementException:
        return True

def do_show_last_msgs(drv):
    user = input('user: ')
    passwd = getpass('password: ')

    if auth(drv, user, passwd):
        for item in show_last_msgs(drv):
            print(
                'title: {}\nissuer: {}\ntimestamp: {}\n'.format(
                    item['title'], item['issuer'], item['timestamp']
                )
            )

def show_last_msgs(drv):
    max_msgs = 20
    offset = 3
    fmt = '//*[@id="ctl00_ContentPlaceHolderPrincipal_' \
        'wucMensagens1_grdMensagens"]/tbody/tr[{}]/td[{}]'

    drv.get('https://qacademico.ifce.edu.br/qacademicodotnet/mensagens.aspx')

    for i in range(offset, offset + max_msgs):
        try:
            title = drv.find_element(by=By.XPATH, value=fmt.format(i, 5))
            issuer = drv.find_element(by=By.XPATH, value=fmt.format(i, 6))
            timestamp = drv.find_element(by=By.XPATH, value=fmt.format(i, 7))

            yield {
                'title': title.text,
                'issuer': issuer.text,
                'timestamp': timestamp.text
            }
        except NoSuchElementException:
            break

def parse_args():
    parser = ArgumentParser(prog='pyfce')

    parser.add_argument(
        '-c',
        '--check-credentials',
        help='check the provided credentials',
        action='store_true'
    )

    parser.add_argument(
        '-m',
        '--check-matriculation',
        help='check if the matriculation is available',
        action='store_true'
    )

    parser.add_argument(
        '-s',
        '--show-last-msgs',
        help='show the last inbox messages',
        action='store_true'
    )

    # no arguments were provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()

def main(args):
    if args:
        op = ChromeOptions()
        op.add_argument('headless')

        drv = Chrome(options=op)
        drv.set_page_load_timeout(10)

        if args.check_credentials:
            do_auth(drv)
        if args.show_last_msgs:
            do_show_last_msgs(drv)
        if args.check_matriculation:
            do_is_matriculation_available(drv)

if __name__ == "__main__":
    try:
        args = parse_args()

        main(args)
    except Exception as err:
        print(err)
        exit(1)
