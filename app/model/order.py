
import uuid

class Order:
  def __init__(self, order_item, price, quantity, location, payment, phone_number, status, username):
    self.order_id = uuid.uuid4().hex
    self.order_item = order_item
    self.price = price
    self.quantity = quantity
    self.location = location
    self.payment = payment
    self.phone_number = phone_number
    self.status = status
    self.username = username

  def to_dict(self):
    return self.__dict__

  def __str__(self):
    return str(self.__dict__)