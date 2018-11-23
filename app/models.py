from flask_sqlalchemy.model import s
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Permission:
    ACCESS = 1
    ADD_USER = 2


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    real_name = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    status_id = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.ACCESS],
            'Admin': [Permission.ACCESS, Permission.ADD_USER],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name
