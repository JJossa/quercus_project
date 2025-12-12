from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# -------------------------
# TABLA ROLE
# -------------------------
class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    permissions = db.Column(db.Text)

    users = db.relationship('User', back_populates='role')


# -------------------------
# TABLA USERS
# -------------------------
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    # 👇 OJO: estos nombres coinciden con tu script SQL
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    role = db.relationship('Role', back_populates='users')
    registrations = db.relationship('Registration', back_populates='user')
    notifications = db.relationship('Notification', back_populates='user')
    access_entries = db.relationship('AccessControl', back_populates='user')


# -------------------------
# TABLA EVENT
# -------------------------
class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time)
    location = db.Column(db.String(200))
    category = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(50))

    registrations = db.relationship('Registration', back_populates='event')
    notifications = db.relationship('Notification', back_populates='event')
    reports = db.relationship('Report', back_populates='event')

    def to_dict(self):
        # 👇 Claves pensadas para el front actual (JS de eventos.html)
        return {
            "id": self.event_id,
            "titulo": self.title,
            "descripcion": self.description,
            "fecha": self.date.strftime("%Y-%m-%d") if self.date else None,
            "hora": self.time.strftime("%H:%M") if self.time else None,
            # extras que igual pueden servir más adelante:
            "lugar": self.location,
            "categoria": self.category,
            "capacidad": self.capacity,
            "status": self.status,
        }



# -------------------------
# TABLA REPORT
# -------------------------
class Report(db.Model):
    __tablename__ = 'report'

    report_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    total_registrations = db.Column(db.Integer)
    confirmed_attendance = db.Column(db.Integer)
    total_payments = db.Column(db.Numeric(12, 2))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship('Event', back_populates='reports')


# -------------------------
# TABLA NOTIFICATION
# -------------------------
class Notification(db.Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    message = db.Column(db.Text)
    type = db.Column(db.String(50))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='notifications')
    event = db.relationship('Event', back_populates='notifications')


# -------------------------
# TABLA REGISTRATION
# -------------------------
class Registration(db.Model):
    __tablename__ = 'registration'

    registration_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    registration_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(50))
    qr_code = db.Column(db.Text)

    user = db.relationship('User', back_populates='registrations')
    event = db.relationship('Event', back_populates='registrations')
    payments = db.relationship('Payment', back_populates='registration')


# -------------------------
# TABLA PAYMENT
# -------------------------
class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.registration_id'))
    amount = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(50))
    transaction_date = db.Column(db.Date, default=datetime.utcnow)
    payment_reference = db.Column(db.Text)

    registration = db.relationship('Registration', back_populates='payments')


# -------------------------
# TABLA ACCESS CONTROL
# -------------------------
class AccessControl(db.Model):
    __tablename__ = 'access_control'

    access_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    token = db.Column(db.Text)

    user = db.relationship('User', back_populates='access_entries')

