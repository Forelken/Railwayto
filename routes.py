from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from tables import *
from config import app
from export import *


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return 'Access Denied', 403

    tables = db.get_tables()
    if request.method == 'POST':
        selected_table = request.form.get('table')
        if 'export_xlsx' in request.form:
            return export_to_xlsx(selected_table)
        elif 'export_json' in request.form:
            return export_to_json(selected_table)

    with open('db_app.log', 'r') as file:
        logs = file.readlines()[-50:]
        logs.reverse() 
        
    return render_template('admin.html', logs=logs, tables=tables, admin_header=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_or_none(User.username == username)
        if user and user.check_password(password):
            logging.info(f'User {username} logged in.')
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logging.info(f'User {current_user.username} logged out.')
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return 'Access Denied', 403
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        user = User.create(username=username, is_admin=is_admin)
        user.set_password(password)
        user.save()
        logging.info(f'User {username} created by {current_user.username}.')
        return redirect(url_for('admin'))
    return render_template('create_user.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/directions_base')
def directions_base():
    search = request.args.get('search', '')

    if search:
        # Небезопасный способ формирования SQL-запроса
        query = f"""
            SELECT direction.direction_id AS direction_id, direction.start AS start, direction.finish AS finish, direction.time AS time, direction.distance AS distance
            FROM direction
            WHERE direction.start LIKE '{search}' OR direction.finish LIKE '{search}' 
        """
    else:
        # Запрос для отображения всех записей
        query = f"""
            SELECT direction.*, COUNT(train.train_id) AS train_count
            FROM direction
            LEFT JOIN train ON direction.direction_id = train.direction_id
            GROUP BY direction.direction_id, direction.start, direction.finish, direction.time, direction.distance
        """

    cursor = db.execute_sql(query)
    directions = [
        {
            'direction_id': row[0],
            'start': row[1],
            'finish': row[2],
            'time': row[3],
            'distance': row[4],
        }
        for row in cursor.fetchall()
    ]

    return render_template('directions_base.html', directions=directions, search=search)

@app.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket(): 
    direction_id = request.args.get('direction_id')
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        email = request.form['email']
        seat_id = request.form['seat_id']
        date = request.form['date']
        ticket_office_id = request.form['ticket_office_id']

        seat = Seat.get(Seat.seat_id == seat_id)

        direction = Direction.get(Direction.direction_id == direction_id)

        sale_credits = direction.distance * 15

        customer = Customer.create(name=name, surname=surname, phone=phone, email=email)

        ticket = Ticket.create(date=date, direction_id=direction_id, seat_id=seat_id, train_id=seat.train, customer=customer)

        sale = Sale.create(sale_credits=sale_credits, date=date, ticket_office_id=ticket_office_id, ticket=ticket)

        return redirect(url_for('index'))

    directions = Direction.select()
    seats = Seat.select().join(Train).where(Train.direction_id == direction_id)
    ticket_offices = TicketOffice.select()
    direction = Direction.get(Direction.direction_id == direction_id)

    return render_template('buy_ticket.html', directions=directions, ticket_offices=ticket_offices, seats=seats, direction_id=direction_id, direction=direction)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/customers', methods=['GET'])
@login_required
def get_customers():
    if not current_user.is_admin:
        return 'Access Denied', 403
    customers = Customer.select().order_by(Customer.customer_id)
    customers_list = [customer.to_dict() for customer in customers]
    return render_template('customers.html', customers=customers_list, admin_header=True)

@app.route('/customers/<int:pk>', methods=['GET'])
@login_required
def get_customer(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        customer = Customer.get(Customer.customer_id == pk)
        return render_template('customer_detail.html', customer=customer.to_dict(), admin_header=True)
    except Customer.DoesNotExist:
        return 'Customer not found', 404

@app.route('/ticket_offices', methods=['GET'])
@login_required
def get_ticket_offices():
    if not current_user.is_admin:
        return 'Access Denied', 403
    ticket_offices = TicketOffice.select().order_by(TicketOffice.ticket_office_id)
    ticket_offices_list = [office.to_dict() for office in ticket_offices]
    return render_template('ticket_offices.html', ticket_offices=ticket_offices_list, admin_header=True)

@app.route('/ticket_offices/<int:pk>', methods=['GET'])
@login_required
def get_ticket_office(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        ticket_office = TicketOffice.get(TicketOffice.ticket_office_id == pk)
        return render_template('ticket_office_detail.html', ticket_office=ticket_office.to_dict(), admin_header=True)
    except TicketOffice.DoesNotExist:
        return 'Ticket Office not found', 404

@app.route('/directions', methods=['GET'])
@login_required
def get_directions():
    if not current_user.is_admin:
        return 'Access Denied', 403
    directions = Direction.select().order_by(Direction.direction_id)
    directions_list = [direction.to_dict() for direction in directions]
    return render_template('directions.html', directions=directions_list, admin_header=True)

@app.route('/directions/<int:pk>', methods=['GET'])
@login_required
def get_direction(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        direction = Direction.get(Direction.direction_id == pk)
        return render_template('direction_detail.html', direction=direction.to_dict(), admin_header=True)
    except Direction.DoesNotExist:
        return 'Direction not found', 404

@app.route('/trains', methods=['GET'])
@login_required
def get_trains():
    if not current_user.is_admin:
        return 'Access Denied', 403
    trains = Train.select().order_by(Train.train_id)
    trains_list = [train.to_dict() for train in trains]
    return render_template('trains.html', trains=trains_list, admin_header=True)

@app.route('/trains/<int:pk>', methods=['GET'])
@login_required
def get_train(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        train = Train.get(Train.train_id == pk)
        return render_template('train_detail.html', train=train.to_dict(), admin_header=True)
    except Train.DoesNotExist:
        return 'Train not found', 404

@app.route('/seats', methods=['GET'])
@login_required
def get_seats():
    if not current_user.is_admin:
        return 'Access Denied', 403
    seats = Seat.select().order_by(Seat.seat_id)
    seats_list = [seat.to_dict() for seat in seats]
    return render_template('seats.html', seats=seats_list, admin_header=True)

@app.route('/seats/<pk>', methods=['GET'])
@login_required
def get_seat(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        seat = Seat.get(Seat.seat_id == pk)
        return render_template('seat_detail.html', seat=seat.to_dict(), admin_header=True)
    except Seat.DoesNotExist:
        return 'Seat not found', 404

@app.route('/tickets', methods=['GET'])
@login_required
def get_tickets():
    if not current_user.is_admin:
        return 'Access Denied', 403
    tickets = Ticket.select().order_by(Ticket.ticket_id)
    tickets_list = [ticket.to_dict() for ticket in tickets]
    return render_template('tickets.html', tickets=tickets_list, admin_header=True)

@app.route('/tickets/<int:pk>', methods=['GET'])
@login_required
def get_ticket(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        ticket = Ticket.get(Ticket.ticket_id == pk)
        return render_template('ticket_detail.html', ticket=ticket.to_dict(), admin_header=True)
    except Ticket.DoesNotExist:
        return 'Ticket not found', 404

@app.route('/sales', methods=['GET'])
@login_required
def get_sales():
    if not current_user.is_admin:
        return 'Access Denied', 403
    sales = Sale.select().order_by(Sale.sale_id)
    sales_list = [sale.to_dict() for sale in sales]
    return render_template('sales.html', sales=sales_list, admin_header=True)

@app.route('/sales/<int:pk>', methods=['GET'])
@login_required
def get_sale(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        sale = Sale.get(Sale.sale_id == pk)
        return render_template('sale_detail.html', sale=sale.to_dict(), admin_header=True)
    except Sale.DoesNotExist:
        return 'Sale not found', 404

@app.route('/update_cell', methods=['POST'])
@login_required
def update_cell():
    if not current_user.is_admin:
        return 'Access Denied', 403
    data = request.get_json()
    table = data['table']
    pk = data['pk']
    field = data['field']
    value = data['value']

    try:
        if table == 'Customer':
            customer = Customer.get(Customer.customer_id == pk)
            setattr(customer, field, value)
            customer.save()
        elif table == 'TicketOffice':
            office = TicketOffice.get(TicketOffice.ticket_office_id == pk)
            setattr(office, field, value)
            office.save()
        elif table == 'Direction':
            direction = Direction.get(Direction.direction_id == pk)
            setattr(direction, field, value)
            direction.save()
        elif table == 'Train':
            train = Train.get(Train.train_id == pk)
            setattr(train, field, value)
            train.save()
        elif table == 'Seat':
            seat = Seat.get(Seat.seat_id == pk)
            setattr(seat, field, value)
            seat.save()
        elif table == 'Ticket':
            ticket = Ticket.get(Ticket.ticket_id == pk)
            setattr(ticket, field, value)
            ticket.save()
        elif table == 'Sale':
            sale = Sale.get(Sale.sale_id == pk)
            setattr(sale, field, value)
            sale.save()
        logging.info(f'Updated {table} {pk}: {field} = {value}')
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f'Error updating cell: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/sort_table', methods=['POST'])
@login_required
def sort_table():
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        data = request.get_json()
        print('Received data:', data)

        table = data.get('table')
        field = data.get('field')
        order = data.get('order')

        if not table or not field or not order:
            return jsonify({'error': 'Missing parameters'}), 400

        if table == 'customer':
            if order == 'asc':
                customers = Customer.select().order_by(getattr(Customer, field))
            else:
                customers = Customer.select().order_by(getattr(Customer, field).desc())
            customers_list = [customer.to_dict() for customer in customers]
            return render_template('sorts/customers_body.html', customers=customers_list)

        elif table == 'ticketoffice':
            if order == 'asc':
                ticket_offices = TicketOffice.select().order_by(getattr(TicketOffice, field))
            else:
                ticket_offices = TicketOffice.select().order_by(getattr(TicketOffice, field).desc())
            ticket_offices_list = [office.to_dict() for office in ticket_offices]
            return render_template('sorts/ticket_offices_body.html', ticket_offices=ticket_offices_list)

        elif table == 'direction':
            if order == 'asc':
                directions = Direction.select().order_by(getattr(Direction, field))
            else:
                directions = Direction.select().order_by(getattr(Direction, field).desc())
            directions_list = [direction.to_dict() for direction in directions]
            return render_template('sorts/directions_body.html', directions=directions_list)

        elif table == 'train':
            if order == 'asc':
                trains = Train.select().order_by(getattr(Train, field))
            else:
                trains = Train.select().order_by(getattr(Train, field).desc())
            trains_list = [train.to_dict() for train in trains]
            return render_template('sorts/trains_body.html', trains=trains_list)

        elif table == 'seat':
            if order == 'asc':
                seats = Seat.select().order_by(getattr(Seat, field))
            else:
                seats = Seat.select().order_by(getattr(Seat, field).desc())
            seats_list = [seat.to_dict() for seat in seats]
            return render_template('sorts/seats_body.html', seats=seats_list)

        elif table == 'ticket':
            if order == 'asc':
                tickets = Ticket.select().order_by(getattr(Ticket, field))
            else:
                tickets = Ticket.select().order_by(getattr(Ticket, field).desc())
            tickets_list = [ticket.to_dict() for ticket in tickets]
            return render_template('sorts/tickets_body.html', tickets=tickets_list)

        elif table == 'sale':
            if order == 'asc':
                sales = Sale.select().order_by(getattr(Sale, field))
            else:
                sales = Sale.select().order_by(getattr(Sale, field).desc())
            sales_list = [sale.to_dict() for sale in sales]
            return render_template('sorts/sales_body.html', sales=sales_list)

        elif table == 'user':
            if order == 'asc':
                users = User.select().order_by(getattr(User, field))
            else:
                users = User.select().order_by(getattr(User, field).desc())
            users_list = [user.to_dict() for user in users]
            return render_template('sorts/users_body.html', users=users_list)
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    if not current_user.is_admin:
        return 'Access Denied', 403
    users = User.select().order_by(User.id)
    users_list = [user.to_dict() for user in users]
    return render_template('users.html', users=users_list, admin_header=True)

@app.route('/users/<int:pk>', methods=['GET'])
@login_required
def get_user(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        user = User.get(User.id == pk)
        return render_template('user_detail.html', user=user.to_dict(), admin_header=True)
    except User.DoesNotExist:
        return 'User not found', 404

@app.route('/users/toggle_admin/<int:pk>', methods=['POST'])
@login_required
def toggle_admin(pk):
    if not current_user.is_admin:
        return 'Access Denied', 403
    try:
        user = User.get(User.id == pk)
        
        print(user)
        
        user.is_admin = not user.is_admin
        user.save()
        logging.info(f'Toggled admin status for user {user.username}.')
        return jsonify({'success': True})
    except User.DoesNotExist:
        return jsonify({'success': False, 'error': 'User not found'}), 404

@app.route('/<table_name>/<int:pk>/delete', methods=['POST'])
@login_required
def delete_item(table_name, pk):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Access Denied'}), 403

    try:
        if table_name == 'users':
            item = User.get(User.id == pk)
        elif table_name == 'customers':
            item = Customer.get(Customer.customer_id == pk)
        elif table_name == 'ticket_offices':
            item = TicketOffice.get(TicketOffice.ticket_office_id == pk)
        elif table_name == 'directions':
            item = Direction.get(Direction.direction_id == pk)
        elif table_name == 'train':
            item = Train.get(Train.train_id == pk)
        elif table_name == 'seat':
            item = Seat.get(Seat.seat_id == pk)
        elif table_name == 'ticket':
            item = Ticket.get(Ticket.ticket_id == pk)
        elif table_name == 'sale':
            item = Sale.get(Sale.sale_id == pk)
        else:
            return jsonify({'success': False, 'error': 'Invalid table name'}), 400
        
        item.delete_instance()
        app.logger.info(f'Deleted {table_name} with id {pk}.')
        return jsonify({'success': True})
    except DoesNotExist:
        return jsonify({'success': False, 'error': f'{table_name.capitalize()} not found'}), 404
    except Exception as e:
        app.logger.error(f'Error deleting {table_name} with id {pk}: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500
       
@app.route('/create_item', methods=['POST'])
@login_required
def create_item():
    data = request.get_json()
    table_name = data.get('table')
    fields = data.get('fields')

    print(f"Received data: {data}") 

    if not table_name or not fields:
        return jsonify(success=False, error='Invalid data'), 400

    try:
        if table_name == 'customer':
            new_item = Customer(**fields)
            new_item.save()
        elif table_name == 'ticketoffice':
            new_item = TicketOffice.create(**fields)
            new_item.save()
        elif table_name == 'direction':
            new_item = Direction(**fields)
            new_item.save()
        elif table_name == 'train':
            new_item = Train.create(**fields)
            new_item.save()
        elif table_name == 'seat':
            new_item = Seat(**fields)
            new_item.save()
        elif table_name == 'ticket':
            new_item = Ticket.create(**fields)
        elif table_name == 'sale':
            new_item = Sale.create(**fields)
        else:
            return jsonify(success=False, error='Invalid table name'), 400

        return jsonify(success=True, id=new_item.id, **fields)
    except Exception as e:
        print(f"Error creating item: {e}") 
        return jsonify(success=False, error=str(e)), 500

@app.route('/get_seats_for_<int:pk>', methods=['GET'])
def get_seats_place(pk):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Access Denied'}), 403 
    
    direction_id = pk
    seats = Seat.select().join(Train).where(Train.direction_id == direction_id)
    seats_data = [{'seat_id': seat.seat_id, 'class_field': seat.class_field, 'seat_place': seat.seat_place, 'carriage': seat.carriage, 'train_id': seat.train_id} for seat in seats]
    return jsonify(seats_data)