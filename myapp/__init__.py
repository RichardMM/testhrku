


from flask import Flask
from flask_mail import Mail
from logging import FileHandler, WARNING
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, DOCUMENTS, TEXT, configure_uploads
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


handler = FileHandler("error.txt")
handler.setLevel(level=WARNING)
app = Flask(__name__)

#set logging details

app.logger.addHandler(handler)

app.config.from_pyfile(filename='config.py')

mail = Mail(app=app)


extensions = extensions=('txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml')
files = UploadSet(name="files", extensions=extensions, default_dest=lambda app: app.instance_path)
configure_uploads(app, files)
db = SQLAlchemy(app=app)
migrater = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

from myapp.warehouse.views import warehouse_mod
from myapp import models
from myapp.warehouse import posts
#db.drop_all()
db.create_all()

app.register_blueprint(warehouse_mod)
