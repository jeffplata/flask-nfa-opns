import datetime
from flask import current_app
from flask_script import Command
from app import db
from app.user_models import User, Role

from app.models import Commodity, Container, Variety, Item

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()


def init_db():
    """ Initialize the database."""
    # activate drop_all and create_all if not using alembic
    # db.drop_all()
    # db.create_all()
    create_users()

    create_app_data()


def create_app_data():
    """ Crate seed data for application """

    local_rice = find_or_create_commodity('Local Rice', True)
    local_palay = find_or_create_commodity('Local Palay', True)

    find_or_create_container('PPRG50', 'G50', 0.78)
    find_or_create_container('PPRE50', 'E50', 0.86)

    find_or_create_variety('WD1', local_rice)
    find_or_create_variety('WD2', local_rice)
    find_or_create_variety('PD1', local_palay)
    find_or_create_variety('PD3', local_palay)

    find_or_create_item('WD1', local_rice)
    db.session.commit()


def find_or_create_commodity(name, is_cereal):
    """ Create Commodity """
    commodity = Commodity.query.filter(Commodity.comm_name == name).first()
    if not commodity:
        commodity = Commodity(comm_name=name, is_cereal=is_cereal)
        db.session.add(commodity)
    return commodity


def find_or_create_container(name, short_name, weight):
    """ Create Container """
    container = Container.query.filter(Container.cont_name == name).first()
    if not container:
        container = Container(cont_name=name, cont_short_name=short_name, weight=weight)
        db.session.add(container)
    return container


def find_or_create_variety(name, commodity):
    """ Create Container """
    variety = Variety.query.filter(Variety.var_name == name).first()
    if not variety:
        variety = Variety(var_name=name, commodity=commodity)
        db.session.add(variety)
    return variety


def find_or_create_item(name):
    """ Find existing role or create new role """
    item = Item.query.filter(Item.item_name == name).first()
    if not item:
        item = Item(name=name)
        db.session.add(item)
    return item


def create_users():
    """ Create users """

    # Adding roles
    admin_role = find_or_create_role('admin', 'Admin')

    # Add users
    find_or_create_user('admin','admin@example.com', 'Password1', admin_role)
    find_or_create_user('member','member@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(username, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(username=username,
                    email=email,
                    password=current_app.user_manager.hash_password(password),
                    is_enabled=True,
                    confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
