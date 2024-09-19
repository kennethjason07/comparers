from flask import Flask, request, jsonify
from flask_cors import CORS
from back.app import app, db
from back.models import Bill, Order
from datetime import datetime
import json



@app.route('/api/new-bill', methods=['POST'])
def new_bill():
    try:
        data = request.get_json()

        def parse_date(date_str):
            try:
                if date_str:
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
                return None
            except ValueError:
                return None

        customer_name = data.get('customerName')
        mobile_number = data.get('mobileNo')
        date_issue = parse_date(data.get('dateIssue', None))
        delivery_date = parse_date(data.get('deliveryDate', None))
        today_date = parse_date(data.get('todayDate', None))
        due_date = parse_date(data.get('dueDate', None))

        garment_type = data.get('garmentType', None)
        suit_qty = data.get('suitQty', 0)
        safari_qty = data.get('safariQty', 0)
        pant_qty = data.get('pantQty', 0)
        shirt_qty = data.get('shirtQty', 0)
        total_qty = data.get('totalQty', 0)
        total_amt = data.get('totalAmt', 0.0)
        payment_mode = data.get('paymentMode', None)
        payment_status = data.get('paymentStatus', None)
        payment_amount = data.get('paymentAmount', 0.0)

        pant_length = data.get('pantLength', None)
        pant_kamar = data.get('pantKamar', None)
        pant_hips = data.get('pantHips', None)
        pant_waist = data.get('pantWaist', None)
        pant_ghutna = data.get('pantGhutna', None)
        pant_bottom = data.get('pantBottom', None)
        pant_seat = data.get('pantSeat', None)

        shirt_length = data.get('shirtLength', None)
        shirt_body = data.get('shirtBody', None)
        shirt_loose = data.get('shirtLoose', None)
        shirt_shoulder = data.get('shirtShoulder', None)
        shirt_astin = data.get('shirtAstin', None)
        shirt_collar = data.get('shirtCollar', None)
        shirt_aloose = data.get('shirtAloose', None)

        extra_measurements = data.get('extraMeasurements', None)
        if isinstance(extra_measurements, dict):
            extra_measurements = json.dumps(extra_measurements)  # Convert dict to JSON string

        new_bill = Bill(
            customer_name=customer_name,
            mobile_number=mobile_number,
            date_issue=date_issue,
            delivery_date=delivery_date,
            garment_type=garment_type,
            suit_qty=suit_qty,
            safari_qty=safari_qty,
            pant_qty=pant_qty,
            shirt_qty=shirt_qty,
            total_qty=total_qty,
            today_date=today_date,
            due_date=due_date,
            total_amt=total_amt,
            payment_mode=payment_mode,
            payment_status=payment_status,
            payment_amount=payment_amount,
            pant_length=pant_length,
            pant_kamar=pant_kamar,
            pant_hips=pant_hips,
            pant_waist=pant_waist,
            pant_ghutna=pant_ghutna,
            pant_bottom=pant_bottom,
            pant_seat=pant_seat,
            shirt_length=shirt_length,
            shirt_body=shirt_body,
            shirt_loose=shirt_loose,
            shirt_shoulder=shirt_shoulder,
            shirt_astin=shirt_astin,
            shirt_collar=shirt_collar,
            shirt_aloose=shirt_aloose,
            extra_measurements=extra_measurements
        )

        db.session.add(new_bill)
        db.session.commit()

        new_order = Order(
            garment_type=garment_type,
            quantity=total_qty,
            status='Pending',
            order_date=datetime.now().date(),
            due_date=due_date,
            payment_mode=payment_mode,
            payment_status=payment_status,
            payment_amount=payment_amount,
            bill_id=new_bill.id
        )

        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Bill and order created successfully', 'bill_id': new_bill.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        # Fetch all orders from the database
        orders = Order.query.all()

        # Create a dictionary to group orders by delivery date
        grouped_orders = {}

        for order in orders:
            # Format the delivery date as a string
            delivery_date = order.due_date.strftime('%Y-%m-%d')

            # If this delivery date is not in the dictionary, add it
            if delivery_date not in grouped_orders:
                grouped_orders[delivery_date] = []

            # Append the order details to the corresponding delivery date
            grouped_orders[delivery_date].append({
                'id': order.id,
                'garment_type': order.garment_type,
                'quantity': order.quantity,
                'status': order.status,
                'order_date': order.order_date.strftime('%Y-%m-%d'),  # Format date as string
                'due_date': order.due_date.strftime('%Y-%m-%d'),  # Format date as string
                'payment_mode': order.payment_mode,
                'payment_status': order.payment_status,
                'payment_amount': order.payment_amount,
                'bill_id': order.bill_id
            })

        # Return the grouped orders as JSON
        return jsonify(grouped_orders), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

        



    

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        status = data.get('status')

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.status = status
        db.session.commit()

        return jsonify({'message': 'Order status updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>/payment-status', methods=['PUT'])
def update_payment_status(order_id):
    try:
        data = request.get_json()
        payment_status = data.get('payment_status')

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.payment_status = payment_status
        db.session.commit()

        return jsonify({'message': 'Payment status updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
