import json
import socket
import secrets
from psycopg2 import connect

global hosts
hosts = []


def find_user(data_dict):
    """A function that search user in database"""

    try:
        conn = connect(
            user='postgres',
            dbname='corpmessenger',
            password='admin',
            host='localhost'
        )
        cur = conn.cursor()
        cur.execute(f'select user_id from users '
                    f'where login = \'{data_dict["login"]}\''
                    f' and password = \'{data_dict["password"]}\'')
        res = cur.fetchone()
        conn.close()
    except Exception as exc:
        print(f'Find user error: {exc}')
        res = None

    # Preparing answer
    if res is not None:
        token = secrets.token_urlsafe(16)
        hosts.append(token)
        answ = {
            "success": True,
            "id": res[0],
            "token": token
        }
    else:
        answ = {
            "success": False
        }

    return answ


def update_users():
    """A function that provides updating users list"""

    try:
        conn = connect(
            user='postgres',
            dbname='corpmessenger',
            password='admin',
            host='localhost'
        )
        cur = conn.cursor()
        cur.execute('select user_id, login from users')
        res = cur.fetchall()
        conn.close()
    except Exception as exc:
        print(f'Update users error: {exc}')
        res = None

    # Preparing answer
    if res is not None:
        answ = {
            "success": True,
            "result": res
        }
    else:
        answ = {
            "success": False
        }

    return answ


def send_mess(data_dict):
    """A function that provides sending message"""

    try:
        conn = connect(
            user='postgres',
            dbname='corpmessenger',
            password='admin',
            host='localhost'
        )
        cur = conn.cursor()

        # Preparing message
        cur.execute(f'select login from users '
                    f'where user_id = {data_dict["from"]}')
        from_user = cur.fetchone()[0]
        msg = f"{from_user}: {data_dict['message']}\n"

        # Finding messages
        cur.execute(f"select exists (select messages from messages_table"
                    f" where from_user_id = {data_dict['from']} "
                    f"and to_user_id = {data_dict['to']})")
        res = cur.fetchone()

        # Saving message in base
        if res[0]:
            # Getting messages for adding another one
            cur.execute(f"select messages from messages_table"
                        f" where from_user_id = {data_dict['from']} "
                        f"and to_user_id = {data_dict['to']}")
            get_result = cur.fetchone()[0]
            msg = get_result + msg

            # Adding new messages
            cur.execute(f"update messages_table "
                        f"set messages = '{msg}' "  #  messages + '{msg}'
                        f"where from_user_id = {data_dict['from']} "
                        f"and to_user_id = {data_dict['to']}")

            cur.execute(f"update messages_table "
                        f"set messages = '{msg}' "
                        f"where from_user_id = {data_dict['to']} "
                        f"and to_user_id = {data_dict['from']}")

        else:
            cur.execute(
                f"insert into messages_table "
                f"(from_user_id, to_user_id, messages) "
                f"values ({data_dict['from']}, {data_dict['to']}, '{msg}')"
            )

            cur.execute(
                f"insert into messages_table "
                f"(from_user_id, to_user_id, messages) "
                f"values ({data_dict['to']}, {data_dict['from']}, '{msg}')"
            )

        conn.commit()
        cur.close()
        conn.close()
    except Exception as exc:
        print(f'Send messages error: {exc}')
        res = None

    # Preparing answer
    if res is not None:
        answ = {
            "success": True
        }
    else:
        answ = {
            "success": False
        }

    return answ


def update_messages(data_dict):
    """A function that provides reading all messages from database"""

    try:
        conn = connect(
            user='postgres',
            dbname='corpmessenger',
            password='admin',
            host='localhost'
        )
        cur = conn.cursor()
        cur.execute(f'select messages from messages_table '
                    f'where from_user_id = {data_dict["from"]} '
                    f'and to_user_id = {data_dict["to"]}')
        res = cur.fetchone()

        cur.close()
        conn.close()
    except Exception as exc:
        print(f'Update messages error: {exc}')
        res = None

    # Preparing answer
    if res is not None:
        answ = {
            "success": True,
            "result": res[0]
        }
    else:
        answ = {
            "success": False
        }
    return answ


# network constants
server_ip = '10.10.1.10'
server_port = 7770

server = socket.socket()
server.bind((server_ip, server_port))
server.listen(5)

while True:
    # Accepting the connection
    con, _ = server.accept()
    payload = con.recv(1024)
    data = payload.decode()
    data = json.loads(data)

    # Answering
    if data["action"] == 'login':
        answer = find_user(data)
    elif data["token"] not in hosts:
        answer = {
            "success": False,
            "error": "Unauthorized user"
        }
    elif data["action"] == 'update_users':
        answer = update_users()
    elif data["action"] == 'send_mess':
        answer = send_mess(data)
    elif data["action"] == 'update_messages':
        answer = update_messages(data)
    else:
        answer = {
            "success": False,
            "error": "Unsupported action",
        }

    answer = json.dumps(answer)
    con.send(answer.encode())
    con.close()
