from argparse import ArgumentParser
from sys import argv, exit

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def do_auth(drv):
    user = input('user: ')
    passwd = input('password: ')

    if auth(drv, user, passwd):
        print('the credentials are valid')
    else:
        print('failed to login with the provided credentials')

def auth(drv, user, passwd):
    drv.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=1001')

    drv.find_element(by=By.XPATH, value='//*[@id="txtLogin"]').send_keys(user)
    drv.find_element(by=By.XPATH, value='//*[@id="txtSenha"]').send_keys(passwd)
    drv.find_element(by=By.XPATH, value='//*[@id="btnOk"]').click()

    # check the authentication result
    try:
        drv.find_element(by=By.XPATH, value='//*[@id="Image1"]')

        return True
    except NoSuchElementException:
        return False

def do_is_matriculation_available(drv):
    user = input('user: ')
    passwd = input('password: ')

    if auth(drv, user, passwd):
        ret = is_matriculation_available(drv)

        if ret:
            print('matriculation available')
        else:
            print('matriculation not available')

def is_matriculation_available(drv):
    no_matriculation_txt = '- Não há nenhuma etapa de pedido de ' \
        'matrícula aberta no momento.'

    drv.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2047')

    try:
        element = drv.find_element(
            by=By.XPATH,
            value='/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]'
                + '/table[2]/tbody/tr/td[2]/span'
        )

        if element.text == no_matriculation_txt:
            return False
    except NoSuchElementException:
        return True

def do_show_inbox(drv, n_msgs):
    user = input('user: ')
    passwd = input('password: ')

    if auth(drv, user, passwd):
        ret = show_inbox(drv, n_msgs)
        for item in ret:
            print(
                'title: {}\nissuer: {}\ntimestamp: {}\n'.format(
                    item['title'], item['issuer'], item['timestamp']
                )
            )

def show_inbox(drv, n_msgs):
    xpath_base = '//*[@id="ctl00_ContentPlaceHolderPrincipal_wucMensagens' \
        '1_grdMensagens"]/tbody/'
    msgs = []

    drv.get('https://qacademico.ifce.edu.br/qacademicodotnet/mensagens.aspx')

    try:
        offset = 3

        for i in range(offset, offset + int(n_msgs)):
            title = drv.find_element(
                by=By.XPATH,
                value='{}/tr[{}]/td[5]'.format(xpath_base, i)
            )
            issuer = drv.find_element(
                by=By.XPATH,
                value='{}/tr[{}]/td[6]'.format(xpath_base, i)
            )
            timestamp = drv.find_element(
                by=By.XPATH,
                value='{}/tr[{}]/td[7]'.format(xpath_base, i)
            )

            msgs.append(
                {
                    'title': title.text,
                    'issuer': issuer.text,
                    'timestamp': timestamp.text
                }
            )
    except NoSuchElementException as err:
        print(err)

    return msgs


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
        '--show-msg-list',
        help='show the list of inbox messages',
        metavar='n_messages'
    )

    # no arguments were provided
    if len(argv) == 1:
        parser.print_help()

    return parser.parse_args()

def main(args):
    op = ChromeOptions()
    op.add_argument('headless')

    drv = Chrome(options=op)
    drv.set_page_load_timeout(10)

    if args.check_credentials:
        do_auth(drv)
    if args.show_msg_list:
        do_show_inbox(drv, args.show_msg_list)
    if args.check_matriculation:
        do_is_matriculation_available(drv)

if __name__ == "__main__":
    try:
        args = parse_args()

        main(args)
    except Exception as err:
        print(err)
        exit(1)
