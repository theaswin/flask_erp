import os
from flask import Flask, Response, redirect, render_template, request, url_for
from sqlalchemy import inspect, text
from models import Customer, db
from sqlalchemy import inspect, text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/my_erp.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ===========================================================================

def init_db():
    with app.app_context():

        # Create tables that don't exist
        db.create_all()

        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        for table in db.metadata.sorted_tables:

            table_name = table.name

            if table_name not in existing_tables:
                continue

            # Columns currently in database
            db_columns = {
                column["name"]
                for column in inspector.get_columns(table_name)
            }

            # Columns defined in SQLAlchemy model
            model_columns = {
                column.name
                for column in table.columns
            }

            # --------------------------------
            # ADD NEW COLUMNS
            # --------------------------------

            new_columns = model_columns - db_columns

            for column_name in new_columns:

                column = table.columns[column_name]

                column_type = column.type.compile(
                    dialect=db.engine.dialect
                )

                sql = f'''
                    ALTER TABLE "{table_name}"
                    ADD COLUMN "{column_name}" {column_type}
                '''

                print(f"Adding column: {table_name}.{column_name}")

                db.session.execute(text(sql))

            # --------------------------------
            # REMOVE OLD COLUMNS
            # --------------------------------

            removed_columns = db_columns - model_columns

            for column_name in removed_columns:

                # Never remove primary key automatically
                if column_name == "id":
                    continue

                print(
                    f"Removing column: {table_name}.{column_name}"
                )

                db.session.execute(text(
                    f'''
                    ALTER TABLE "{table_name}"
                    DROP COLUMN "{column_name}"
                    '''
                ))

        db.session.commit()

# ===========================================================================





@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        image = request.files.get('image')
        customer = Customer(
            image=image.read() if image and image.filename else None,
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customers'))

    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@app.route('/customers/<int:customer_id>/image')
def customer_image(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    if not customer.image:
        return '', 404
    if customer.image.startswith(b'\x89PNG'):
        mimetype = 'image/png'
    elif customer.image.startswith(b'\xff\xd8\xff'):
        mimetype = 'image/jpeg'
    elif customer.image.startswith((b'GIF87a', b'GIF89a')):
        mimetype = 'image/gif'
    elif customer.image.startswith(b'RIFF') and customer.image[8:12] == b'WEBP':
        mimetype = 'image/webp'
    else:
        mimetype = 'application/octet-stream'
    return Response(customer.image, mimetype=mimetype)


@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)