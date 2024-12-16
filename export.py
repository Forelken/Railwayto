from openpyxl import Workbook
import io
import json
from flask import send_file, Response
from peewee import Model
from config import db
from tables import *

tables = {'user': User, 'customer': Customer, 'direction': Direction, 'sale': Sale, 'seat': Seat, 'ticket': Ticket, 'ticketoffice': TicketOffice, 'train': Train}

def export_to_xlsx(selected_table):
    wb = Workbook()
    ws = wb.active

    headers = [field.name for field in tables[selected_table]._meta.sorted_fields]
    ws.append(headers)

    #print(headers)

    # Данные
    for row in tables[selected_table].select():
        ws.append([getattr(row, field) for field in headers])


    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f'{model.__name__}.xlsx')

def export_to_json(selected_table):
    data = []
    headers = [field.name for field in tables[selected_table]._meta.sorted_fields]
    for row in tables[selected_table].select():
        row_data = {field: getattr(row, field) for field in headers}
        data.append(row_data)

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return Response(
        json_data,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={selected_table}.json'}
    )
