from  flask import Blueprint, request, jsonify
import uuid

mod = Blueprint('orders', __name__)
users_list = []
order_list = []

@mod.route('/')
def home():
    print("hello world")
    return jsonify({
        "message": "Welcome to Fast Food Fast"
    }), 200


@mod.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not username or not password or not email:
        return jsonify({
            "error": "Please provide vaild information"
        }), 400
    for user in users_list:
        if username == user["username"]:
            return jsonify({ "message": "Account already exists"
        }), 200

    user = {
        "username": username,
        "email": email,
        "password": password
    }
    users_list.append(user)

    response = {
        "message": "User registered successfully",
        "data": user
    }

    return jsonify(response), 201


@mod.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user =  {
            "username": username,
            "password": password,
        }
    for user in users_list:
        if username == user["username"] and password == user["password"]:
            return jsonify({ "message": "login sucessful"}), 200
        else:
            return jsonify({"message":"invalid information"})    


@mod.route('/order', methods=['POST'])
def create_order():
	data = request.get_json(force = True)

	username = data.get('username', None)
	phone_number = data.get('phone_number', None)
	location = data.get('location', None)
	order_item = data.get('order_item',None)
	payment = data.get('payment', None)

	order = {
		'username': username,
		'phone_number': phone_number,
		'location': location,
		'order_item': order_item,
		"payment": payment,
		"order_id": uuid.uuid4().hex, 
		"status": "Pending"
	}

	resp = validate_order(order)

	if resp:
		return jsonify(resp), 400
	
	order_list.append(order)
	response = {
		"message": "Order created successfully ",
		"data": order
	}
	
	return jsonify(response), 201

def validate_order(order):
	response = {}
	user_exists = False

	if order:
		username = order.get("username", None)
		phone_number = order.get("phone_number", None)
		location = order.get("location", None)
		order_item = order.get("order_item", None)
		payment = order.get("payment", None)

		for user in users_list:
			if username == user["username"]:
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

@mod.route('/order/<int:order_id>',methods=['GET'])
def get_specific(order_id):
    for order in order_list:
        if order["orderid"] == order_id:
            return jsonify({"orders" :order})

@mod.route('/order/<int:order_id>',methods=['PUT'])
def update_order(order_id):

    status = request.json['status']
    for order in order_list:
        if order["orderid"] == order_id:
            order["status"]= status
            return jsonify({"message":"order updated"})
