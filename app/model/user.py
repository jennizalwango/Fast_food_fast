import uuid

class User:
  def __init__(self, username, email, password, frist_name, last_name):
    self.user_id = uuid.uuid4().hex
    self.username = username
    self.email = email
    self.password = password
    self.frist_name = frist_name
    self.last_name = last_name

  def to_dict(self):
    return self.__dict__

  def __str__(self):
    return str(self.to_dict())
