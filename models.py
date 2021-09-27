import bcrypt
import uuid
from hearatale import db, jwt
from datetime import datetime
import secrets


class Teacher(db.Model):
    __tablename__ = "teachers"
    uuid = db.Column(db.Unicode(length=128), primary_key=True, default=uuid.uuid1.__str__)
    username = db.Column(db.Unicode(length=128), unique=True)
    hashed_password = db.Column(db.Unicode(length=128), unique=True)
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

        if u.check_password(password):
            return u

        return None

    @staticmethod
    def register(username, password, email):
        if Teacher.query.filter_by(username=username).count() != 0:
            return "This username has been taken by another user."

        u = Teacher(username=username, password=Teacher.hash_pw(password), email=email)
        u.save()

        return True


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

        return u

    @staticmethod
    def register(name):
        u = Student(name=name, password=secrets.token_hex(3))
        if u is None:
            return False

        u.save()

        return True


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(cls):
    return cls.uuid


# Register a callback function that loades a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    s = Student.query.filter_by(uuid=identity).one_or_none()
    if s:
        return s

    t = Teacher.query.filter_by(uuid=identity).one_or_none()
    return t