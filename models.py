import bcrypt
import uuid
from hearatale import db, login_manager
from datetime import datetime
import secrets


class Teacher(db.Model):
    __tablename__ = "teachers"
    uuid = db.Column(db.Unicode(length=128), primary_key=True, default=uuid.uuid1.__str__)
    username = db.Column(db.Unicode(length=128), unique=True)
    name = db.Column(db.Unicode(length=64), unique=True)
    email = db.Column(db.Unicode(length=128), unique=True)
    joined = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def hash_pw(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

    @staticmethod
    def login(username, password):
        u = Teacher.query.filter_by(username=username).first()
        if u is None:
            return False

        return u.check_password(password)

    @staticmethod
    def register(username, password, email):
        if Teacher.query.filter_by(username=username).count() != 0:
            return "This username has been taken by another user."

        u = Teacher(username=username, password=Teacher.hash_pw(password), email=email)
        u.save()

        return True

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        t = Teacher.query.get(user_id)
        if not t:
            return Student.query.get(user_id)


class Student(db.Model):
    __tablename__ = "students"
    uuid = db.Column(db.Unicode(length=128), primary_key=True, default=str(uuid.uuid1()))
    password = db.Column(db.Unicode(length=128), unique=True)
    name = db.Column(db.Unicode(length=64), unique=True)
    joined = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return password == self.password

    @staticmethod
    def login(password):
        u = Student.query.filter_by(password=password).first()
        if u is None:
            return False

        return u.check_password(password)

    @staticmethod
    def register(name):
        u = Student(name=name, password=secrets.token_hex(3))
        if u is None:
            return False

        u.save()

        return True
