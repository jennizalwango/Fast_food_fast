from  flask import Blueprint, request, jsonify
import uuid
from app.model.order import Order
from app.model.user import User

mod = Blueprint('orders', __name__)
users_list = []
order_list = []
menu_list = []

@mod.route('/')
def home():
    print("hello world")
    return jsonify({
        "message": "Welcome to Fast Food Fast"
    }), 200


@mod.route('/register', methods=['POST'])
def register():
	data = request.get_json(force = True)

	username = data.get('username', None)
	password = data.get('password',None)
	email = data.get('email', None)
	first_name = data.get('first_name', None)
	last_name = data.get('last_name', None)

	if not username or not password or not email:
		return jsonify({
			"error": "Please provide vaild information"
		}), 400

	for user in users_list:
		if username == user.username:
			return jsonify({ "message": "Account already exists"
		}), 200

	user = User(username, email, password, first_name, last_name)
	users_list.append(user)

	response = {
		"message": "User registered successfully",
		"data": user.to_dict()
	}

	return jsonify(response), 201


@mod.route('/login', methods=['POST'])
def login():
	username = request.json['username']
	password = request.json['password']

	for user in users_list:
		if username == user.username and password == user.password:
			return jsonify({ "message": "login sucessful"}), 200
		
	return jsonify({"message":"invalid information"})    


@mod.route('/order', methods=['POST'])
def create_order():
	data = request.get_json(force = True)

	username = data.get('username', None)
	phone_number = data.get('phone_number', None)
	location = data.get('location', None)
	order_item = data.get('order_item',None)
	payment = data.get('payment', None)
	quantity = data.get('quantity', None)
	price = data.get('price', None)
	status = 'pending'

	order = Order(order_item, price, quantity,location, payment, phone_number, status, username)
	resp = validate_order(order)

	if resp:
		return jsonify(resp), 400
	
	order_list.append(order)

	response = {
		"message": "Order created successfully ",
		"data": order.to_dict()
	}
	
	return jsonify(response), 201

def validate_order(order):
	response = {}
	user_exists = False

	if order:
		order_item = order.order_item
		payment = order.payment
		username = order.username
		phone_number = order.phone_number
		location = order.location

		for user in users_list:
			if username == user.username:
				user_exists = True
				break

		if not user_exists:
			response["error"] = "User assigned to the order doesnot exist"
			return response

		if not phone_number.isdigit() or phone_number.strip() == "" or len(phone_number) < 10 or len(phone_number) > 12:
			response["phone_number_error"] = "Wrong phone number format"
			
		if not location:
			response["location_error"] = "Location is missing"
    
		if not payment:
			response["payment_error"] = "Please clear payment"
		
		if not order_item:
			response["order_item_error"] = "Please place your item"
	else:
		response["error"] = "Please provide order details"
	
	return response


@mod.route('/order',methods=['GET'])
def get_all_orders():
    return jsonify({"orders":order_list})

@mod.route('/order/<order_id>',methods=['GET'])
def get_specific(order_id):
	for order in order_list:
		if order.order_id == order_id:
			return jsonify({
				"order" :order.to_dict()
				})

	return jsonify({
		"error": "Order not found"
	}), 404

@mod.route('/order/<order_id>',methods=['PUT'])
def update_order(order_id):
	data = request.get_json(force = True)
	status = data.get('status', None)

	if not status:
		return jsonify({
			"message": "Please provide status"
		}), 400

	for order in order_list:
			if order.order_id == order_id:
					order.status = status
					return jsonify({
						"message":"Order updated",
						"order": order.to_dict()
						}), 202
					
	return jsonify({
		"message": "Order not found"
	}), 404
