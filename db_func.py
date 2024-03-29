from models import db, Fields, Clients, Prizes, Admin, FieldsAndClients
from flask import Blueprint

database = Blueprint('database', __name__)


def add_client(lst):
    new_client = Clients(email=lst[0], name=lst[1], password=lst[2])
    db.session.add(new_client)
    db.session.commit()


def add_admin(lst):
    new_admin = Admin(email=lst[0], name=lst[1], password=lst[2])
    db.session.add(new_admin)
    db.session.commit()


def add_field(lst):
    field = Fields(size=lst[0], name_prize=str(lst[1]), location_ship=str(lst[2]), hits_client='')
    db.session.add(field)
    db.session.commit()


def add_prize(lst):
    prize = Prizes(file=lst[0], name=lst[1], description=lst[2])
    db.session.add(prize)
    db.session.commit()


def get_all_clients():
    clients = Clients.query.all()
    return [[i.id, i.email] for i in clients]


def get_prizes():
    prizes = Prizes.query.all()
    sl = {}
    for i in prizes:
        sl[i.id] = [i.file, i.name, i.description]
    return sl


def update_prize(lst):
    prize = Prizes.query.filter_by(id=lst[0]).first()
    prize.file = lst[1]
    prize.name = lst[2]
    prize.description = lst[3]
    db.session.commit()


def delete_prize(idd):
    prize = Prizes.query.filter_by(id=idd).first()
    db.session.delete(prize)
    db.session.commit()


def create_pole(client_info):
    new_entry = FieldsAndClients(id_client=client_info[0], id_pole=client_info[1], numbers_hits=client_info[2])
    db.session.add(new_entry)
    db.session.commit()


def get_table(id_client):
    result = FieldsAndClients.query(FieldsAndClients.id_pole).filter_by(id_client=id_client).all()
    return [row[0] for row in result]


def get_info_table(id_pole):
    result = []
    for pole_id in id_pole:
        prize_info = Fields.query.filter_by(id=pole_id[0]).first()
        result.append((prize_info.id, prize_info.size, prize_info.numbers_hits,
                       prize_info.name_prize, prize_info.location_prize, prize_info.hit_client))
    return result


def edit_info_table(id_table, edit_info):
    prize_entry = Fields.query.filter_by(id=id_table).first()
    if prize_entry:
        prize_entry.size = edit_info[0]
        prize_entry.name_prize = edit_info[1]
        prize_entry.location_prize = edit_info[2]
        prize_entry.hit_client = edit_info[3]
        db.session.commit()


def edit_numbers_hits(id_client, id_pole):
    data_entry = FieldsAndClients.query.filter_by(id_client=id_client, id_pole=id_pole).first()
    if data_entry:
        current_hits = data_entry.numbers_hits
        new_hits = max(0, current_hits - 1)
        data_entry.numbers_hits = new_hits
        db.session.commit()


def get_id_table():
    latest_id = Fields.query(Fields.id).order_by(Fields.id.desc()).first()
    if latest_id:
        return latest_id[0]
    else:
        return None