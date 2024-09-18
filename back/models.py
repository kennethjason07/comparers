from datetime import date
from back.app import db

class Bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    date_issue = db.Column(db.Date, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    garment_type = db.Column(db.String(50), nullable=False)
    suit_qty = db.Column(db.Integer, default=0)
    safari_qty = db.Column(db.Integer, default=0)
    pant_qty = db.Column(db.Integer, default=0)
    shirt_qty = db.Column(db.Integer, default=0)
    total_qty = db.Column(db.Integer, default=0)
    today_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    total_amt = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)

    pant_length = db.Column(db.Float)
    pant_kamar = db.Column(db.Float)
    pant_hips = db.Column(db.Float)
    pant_waist = db.Column(db.Float)
    pant_ghutna = db.Column(db.Float)
    pant_bottom = db.Column(db.Float)
    pant_seat = db.Column(db.Float)
    
    shirt_length = db.Column(db.Float)
    shirt_body = db.Column(db.Float)
    shirt_loose = db.Column(db.Float)
    shirt_shoulder = db.Column(db.Float)
    shirt_astin = db.Column(db.Float)
    shirt_collar = db.Column(db.Float)
    shirt_aloose = db.Column(db.Float)

    extra_measurements = db.Column(db.Text)

    # Relationship with orders
    orders = db.relationship('Order', backref='bill', lazy=True)

# class Worker(db.Model):
#     __tablename__ = 'workers'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     number = db.Column(db.String(15), nullable=False)
#     due_amount = db.Column(db.Float, nullable=False)
#     amount_paid = db.Column(db.Float, nullable=False, default=0.0)

#     # One-to-many relationship with orders
#     orders = db.relationship('Order', backref='worker', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    garment_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)

    # ForeignKey to Worker table (nullable)
    # worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=True)

    # ForeignKey to Bill table
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)
