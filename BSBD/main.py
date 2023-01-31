"""The main part of program"""
import authorization
import main_window


if __name__ == '__main__':

    user_status = {
        'acc_id': None,
        'login': None,
        'password': None,
        'role': None,
        'enter': False}

    enter = authorization.AuthorizationWindow(user_status)
    if user_status['enter']:
        main_form = main_window.MainWindow(user_status)
