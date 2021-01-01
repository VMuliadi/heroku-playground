import random, string
from bcrypt import hashpw, gensalt, checkpw
from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from pprint import pprint

class Auth:
  __MAGIC_WORDS = "am0Aibiiw4eiB3qu"
  __MAGIC_SEPARATOR = "SprTR"
  __VALIDATED_USERNAME = "USERNAME"
  __VALIDATED_PASSWORD = b'BCRYPTED_PASSWORD'


  def _generate_randstr(self, length):
    return str("".join(random.choice(string.ascii_uppercase \
      + string.ascii_lowercase \
      + string.digits) for _ in range(length)))


  def _create_auth_token(self, username):
    expiration_time = str((datetime.today() + timedelta(minutes=4)).strftime("%s"))
    enc_magic_words = b64encode(self.__MAGIC_WORDS.encode("utf-8")).decode("utf-8") + self.__MAGIC_SEPARATOR + self._generate_randstr(32) + self.__MAGIC_SEPARATOR
    enc_expiration_time = str(b64encode(expiration_time.encode("utf-8")).decode("utf-8")) + self.__MAGIC_SEPARATOR
    return enc_magic_words + enc_expiration_time + self._generate_randstr(16)


  def is_expired(self, token):
    import re
    magic_words_validator = re.compile(r"([0-9A-Za-z]){32}")
    random_payload_validator = re.compile(r"([0-9A-Za-z]){16}")
    expiration_time = int(b64decode(token.split(self.__MAGIC_SEPARATOR)[2]).decode("utf-8"))
    is_token_expired = True if int(datetime.today().strftime("%s")) > expiration_time else False
    magic_words_validated = True if len(re.findall(magic_words_validator, token.split(self.__MAGIC_SEPARATOR)[1])) > 0 else False
    random_payload_validated = True if len(re.findall(random_payload_validator, token.split(self.__MAGIC_SEPARATOR)[-1])) > 0 else False
    return is_token_expired and magic_words_validated and random_payload_validated


  def login_auth(self, username="", password=""):
    response = {}  # init value...
    response["access_token"] = ""
    response["username"] = username
    
    if username != "" or password != "":
      creation_time = datetime.today()
      password = password.encode("utf-8")
      if username == self.__VALIDATED_USERNAME and checkpw(password, self.__VALIDATED_PASSWORD):
        response["access_token"] = self._create_auth_token(username)
    return response
