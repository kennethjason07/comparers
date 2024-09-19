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

        # Parse dates
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        # Extract data from the form
        customer_name = data.get('customerName')
        mobile_number = data.get('mobileNo')
        date_issue = parse_date(data.get('dateIssue'))
        delivery_date = parse_date(data.get('deliveryDate'))
        today_date = parse_date(data.get('todayDate'))
        due_date = parse_date(data.get('dueDate'))

        garment_type = data.get('garmentType')
        suit_qty = data.get('suitQty', 0)
        safari_qty = data.get('safariQty', 0)
        pant_qty = data.get('pantQty', 0)
        shirt_qty = data.get('shirtQty', 0)
        total_qty = data.get('totalQty', 0)
        total_amt = data.get('totalAmt', 0.0)
        payment_mode = data.get('paymentMode')
        payment_status = data.get('paymentStatus')
        payment_amount = data.get('paymentAmount', 0.0)

        # Pant measurements
        pant_length = data.get('pantLength')
        pant_kamar = data.get('pantKamar')
        pant_hips = data.get('pantHips')
        pant_waist = data.get('pantWaist')
        pant_ghutna = data.get('pantGhutna')
        pant_bottom = data.get('pantBottom')
        pant_seat = data.get('pantSeat')

        # Shirt measurements
        shirt_length = data.get('shirtLength')
        shirt_body = data.get('shirtBody')
        shirt_loose = data.get('shirtLoose')
        shirt_shoulder = data.get('shirtShoulder')
        shirt_astin = data.get('shirtAstin')
        shirt_collar = data.get('shirtCollar')
        shirt_aloose = data.get('shirtAloose')

        # Extra measurements
        extra_measurements = data.get('extraMeasurements')

        # Create new bill
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
        print(request.get_json())


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# @app.route('/api/orders', methods=['GET'])
# def get_orders():
#     try:
#         # Retrieve all orders sorted by due_date
#         orders = Order.query.order_by(Order.due_date.asc()).all()

#         # Use defaultdict to group orders by due_date
#         grouped_orders = defaultdict(list)
        
#         for order in orders:
#             due_date_str = order.due_date.strftime('%Y-%m-%d')  # Format date as string
#             grouped_orders[due_date_str].append({
#                 'id': order.id,
#                 'garment_type': order.garment_type,
#                 'quantity': order.quantity,
#                 'status': order.status,
#                 'order_date': order.order_date.strftime('%Y-%m-%d'),  # Format date as string
#                 'due_date': due_date_str,
#                 'payment_mode': order.payment_mode,
#                 'payment_status': order.payment_status,
#                 'payment_amount': order.payment_amount,
#                 'bill_id': order.bill_id
#             })

#         return jsonify(grouped_orders), 200  # Send the data as JSON response

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


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


        

@app.route('/api/update-order-status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.status = new_status
        db.session.commit()

        return jsonify({'message': 'Order status updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/update-payment-status/<int:order_id>', methods=['PUT'])
def update_payment_status(order_id):
    try:
        data = request.get_json()
        new_payment_status = data.get('payment_status')

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.payment_status = new_payment_status
        db.session.commit()

        return jsonify({'message': 'Payment status updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
if __name__ == "__main__":
    app.run(debug=True)
