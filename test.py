from win32com.server.exception import Exception


class NotEnoughFundsException(Exception):
    pass


def make_transaction():
    account = 0
    wyplata = int(input('ile pieniedzy chcesz wyplacic?'))
    if wyplata > account:
        raise NotEnoughFundsException()


if __name__ == '__main__':
    try:
        make_transaction()
    except Exception as e:
        print("Error occurred")
    print("Error")
