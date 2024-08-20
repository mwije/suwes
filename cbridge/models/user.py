from ..extensions import db
from flask_login import UserMixin
from datetime import datetime

from wtforms.validators import DataRequired, Length, Email, Optional

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    name = db.Column(db.String(120), nullable=False)
    date_birth = db.Column(db.Date, nullable=False)
    identification = db.Column(db.String(15), nullable=True)

    telephone = db.Column(db.String(16), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=False)

    date_joined = db.Column(db.Date, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    @classmethod
    def columns(self):
        return User.__table__.columns

    @classmethod
    def columnsNotNullable(self):
        return [col.name for col in User.__table__.columns if not col.nullable]

    def __repr__(self):
            return f'<User: {self.username}, Role: {self.role}>'

    def get_id(self):
        return self.uid

    @classmethod
    def custom_constraints(cls):
        return {
            'username': [Length(min=3, max=50)],
            'password': [Length(min=3, max=30)],
            'email': [Optional(), Email()]
        }
    
    @classmethod
    def valueset(cls):
        return {
            'role': ['client', 'clinician', 'helper', 'admin', 'dev'],
            'active': [True, False]
        }
    
   
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    patients = db.relationship('Patient')
    clinicians = db.relationship('Clinician')
    helpers = db.relationship('Helper')
 

    def has_role(self, role):
        return bool (
            Role.query
            .join(Role.users)
            .filter(User.uid == self.uid)
            .filter(Role.slug == role)
            .count() == 1
        )
    
    def get_roles(self):
        return [role.slug for role in self.roles]


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    slug = db.Column(db.String(10), nullable=False, unique=True)

    users = db.relationship('User', secondary='user_roles', back_populates='roles')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))

    #user = db.relationship('User', back_populates='patients')
    user = db.relationship('User', backref=db.backref('patient', uselist=False))

class Clinician(db.Model):
    __tablename__ = 'clinicians'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))

    user = db.relationship('User', back_populates='clinicians')
    
class Helper(db.Model):
    __tablename__ = 'helpers'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))

    user = db.relationship('User', back_populates='helpers')