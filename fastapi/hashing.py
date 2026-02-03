import bcrypt

password = "hashing_password"
password2= "hashing_password"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
hashed_password2 = bcrypt.hashpw(password2.encode(),'kdjkjdkj')
print(f"Original password: {password}")
print(f"Bcrypt Hashed password: {hashed_password.decode()}")
print(f"Bcrypt Hashed password: {hashed_password2.decode()}")
salt = bcrypt.gensalt()

print("salt:",salt)
print("salt:",salt.decode())
user_input= "hashing_password"
is_match = bcrypt.checkpw(user_input.encode(), stored_hash)
