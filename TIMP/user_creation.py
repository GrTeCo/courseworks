from psycopg2 import connect
import hashlib as hsh


def make_hash(psswd):
    """Function that provides hashing the password"""

    enc_pass = hsh.md5(psswd.encode('utf-8'))
    return enc_pass.hexdigest()


if __name__ == '__main__':
    login = input('Enter user\'s login: ')
    passwd = input('Enter user\'s password: ')

    hash_pass = make_hash(passwd)

    try:
        conn = connect(
            user='postgres',
            dbname='corpmessenger',
            password='admin',
            host='localhost'
        )
        cur = conn.cursor()

        cur.execute(f'insert into users (login, password) '
                    f'values (\'{login}\', \'{hash_pass}\')')

        conn.commit()
        cur.close()
        conn.close()
    except Exception as exc:
        print(f'Error: {exc}')
