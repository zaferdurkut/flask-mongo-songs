from flask_script import Manager, Server

from config.config import Config
from run import app

server = Server(host=Config.HOST, port=Config.PORT)

manager = Manager(app)
manager.add_command("runserver", server)

if __name__ == "__main__":
    manager.run()
