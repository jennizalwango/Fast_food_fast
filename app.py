from flask import Flask, request, jsonify

app = Flask(__name__)
users_list = []
order_list = []



@app.route('/')
def home():
    print("hello world")
    return jsonify({
        "message": "Welcome to Fast Food Fast"
    }), 200


@app.route('/api/v1/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not username or not password or not email:
        return jsonify({
            "error": "Please provide vaild information"
        }), 400
    # if username ,password,email
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


@app.route('/api/v1/login', methods=['POST'])
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
    
   


@app.route('/api/v1/order', methods=['POST'])
def create_order():
    username = request.json['username']
    phone_number = request.json['phone_number']
    location = request.json['location']
    order_item = request.json['order_item']
    payment = request.json['payment']
    status = request.json['status']
    
    for user in users_list:
        if username == user["username"]:
            if not phone_number.isdigit() or phone_number.strip() == "" or len(phone_number) < 10 or len(phone_number) > 12:
                    return jsonify({'error': 'wrong phone number format'}), 403
                
            if not location:
                    return jsonify({'error': 'location is missing'}), 403
            order_id = len(order_list)+1
            order = {
                'username': username,
                'phonenumber': 123,
                'location': location,
                'order_item': order_item,
                "payment": payment,
                "orderid":order_id,
                "status": status
                }

            order_list.append(order)

            response = {
                "message": "order being processed",
                "data": order
                }
            return jsonify(response)

@app.route('/api/v1/order',methods=['GET'])
def get_all_orders():
    return jsonify({"orders":order_list})

@app.route('/api/v1/order/<int:order_id>',methods=['GET'])
def get_specific(order_id):
    for order in order_list:
        if order["orderid"] == order_id:
            return jsonify({"orders" :order})

            



@app.route('/api/v1/order/<int:order_id>',methods=['PUT'])
def update_order(order_id):

    status = request.json['status']
    for order in order_list:
        if order["orderid"] == order_id:
            order["status"]= status
            return jsonify({"message":"order updated"})






app.run(debug=True)

