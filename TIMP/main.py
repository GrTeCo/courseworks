from authorization import AuthorizationWindow
from MainForm import MainWindow

if __name__ == '__main__':
    user_status = {
        'acc_id': None,
        'login': None,
        'token': None,
        'enter': False
    }
    auth = AuthorizationWindow(user_status)

    if user_status['enter']:
        app = MainWindow(user_status)
    # app = MainWindow(user_status)
