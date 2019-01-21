from os import environ
from Ung_dung import app
if __name__=="__main__":
    # doi localhost thanh ten mien khi chay chinh thuc
    HOST=environ.get('SERVER_HOST','localhost')
    try:
        PORT = int(environ.get('SEVER_PORT','6789'))
    # neu khong tim thay port thì gán cho port
    except ValueError:
        PORT=6789
    app.debug = True
    app.run(HOST,PORT)