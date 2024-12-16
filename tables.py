from peewee import Model, IntegerField, CharField, FloatField, TimeField, DateField, BooleanField, ForeignKeyField, AutoField,  DoesNotExist, fn
import re
from config import db, model
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import logging

bcrypt = Bcrypt()

class RequestFilter(logging.Filter):
    def filter(self, record):
        # Исключаем логи HTTP-запросов
        return 'HTTP' not in record.msg

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler('db_app.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addFilter(RequestFilter())

class User(UserMixin, model):
    username = CharField()
    password = CharField(default='password')
    is_admin = BooleanField(default=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def save(self, *args, **kwargs):
        if self.id:
            logging.info(f'Updated user {self.username} in the database.')
        else:
            logging.info(f'Created user {self.username} in the database.')
        super(User, self).save(*args, **kwargs)

    class Meta:
        database = db  # Убедитесь, что у вас есть объект db для подключения к базе данных

class Customer(model):
    customer_id = AutoField()
    name = CharField(max_length=255)
    surname = CharField(max_length=255)
    phone = CharField(max_length=50)
    email = CharField(max_length=255)

    def validate_phone(self):
        pattern = re.compile(r'^8\d{10}$')
        if not pattern.match(self.phone):
            raise ValueError("Phone number must start with '8' and be followed by 10 digits.")

    def save(self, *args, **kwargs):
        if self.customer_id:
            logging.info(f'Updated customer {self.customer_id} in the database.')
        else:
            logging.info(f'Created customer {self.name} {self.surname} in the database.')
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        database = db

class TicketOffice(model):
    ticket_office_id = AutoField(primary_key=True)
    place = CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.ticket_office_id:
            logging.info(f'Updated ticket office {self.ticket_office_id} in the database.')
        else:
            logging.info(f'Created ticket office at {self.place} in the database.')
        super(TicketOffice, self).save(*args, **kwargs)

    class Meta:
        database = db

class Direction(model):
    direction_id = AutoField(primary_key=True)
    start = CharField(max_length=255)
    finish = CharField(max_length=255)
    time = TimeField()
    distance = FloatField()

    def save(self, *args, **kwargs):
        if self.direction_id:
            logging.info(f'Updated direction {self.direction_id} in the database.')
        else:
            logging.info(f'Created direction from {self.start} to {self.finish} in the database.')
        super(Direction, self).save(*args, **kwargs)

    class Meta:
        database = db

class Train(model):
    train_id = AutoField(primary_key=True)
    train_type = CharField(max_length=255)
    rate = FloatField(default=0.0)
    direction = ForeignKeyField(Direction, backref='trains', null=True, on_delete='SET NULL', on_update='CASCADE')

    def save(self, *args, **kwargs):
        if self.train_id:
            logging.info(f'Updated train {self.train_id} in the database.')
        else:
            logging.info(f'Created train of type {self.train_type} in the database.')
        super(Train, self).save(*args, **kwargs)

    class Meta:
        database = db

class Seat(model):
    seat_id = AutoField()
    class_field = CharField(max_length=255)
    seat_place = IntegerField()
    carriage = IntegerField()
    train = ForeignKeyField(Train, backref='seats', on_delete='CASCADE', on_update='CASCADE')
     

    def save(self, *args, **kwargs):
        if self.seat_id:
            logging.info(f'Updated seat {self.seat_id} in the database.')
        else:
            logging.info(f'Created seat {self.seat_id} in the database.')
        super(Seat, self).save(*args, **kwargs)

    class Meta:
        database = db

class Ticket(model):
    ticket_id = AutoField(primary_key=True)
    date = DateField(null=False)
    direction = ForeignKeyField(Direction, backref='tickets', null=True, on_delete='SET NULL')
    train = ForeignKeyField(Train, backref='tickets', null=True, on_delete='SET NULL')
    seat = ForeignKeyField(Seat, backref='tickets', null=True, on_delete='SET NULL')
    customer = ForeignKeyField(Customer, backref='tickets', on_delete='CASCADE', on_update='CASCADE')

    def save(self, *args, **kwargs):
        if self.ticket_id:
            logging.info(f'Updated ticket {self.ticket_id} in the database.')
        else:
            logging.info(f'Created ticket for customer {self.customer.name} {self.customer.surname} in the database.')
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        database = db

class Sale(model):
    sale_id = AutoField(primary_key=True)
    sale_credits = FloatField(null=False)
    date = DateField(null=False)
    ticket_office = ForeignKeyField(TicketOffice, backref='sales', null=True, on_delete='SET NULL')
    ticket = ForeignKeyField(Ticket, backref='sales', on_delete='CASCADE', on_update='CASCADE')

    def save(self, *args, **kwargs):
        if self.sale_id:
            logging.info(f'Updated sale {self.sale_id} in the database.')
        else:
            logging.info(f'Created sale for {self.sale_credits} credits in the database.')
        super(Sale, self).save(*args, **kwargs)

    class Meta:
        database = db

# Создание таблиц в базе данных
with db:
    db.create_tables([User, Customer, TicketOffice, Direction, Train, Seat, Ticket, Sale])
