from sanic_motor import BaseModel
# import hashlib
# from utils import create_hash

class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['name', 'password']
         
    
    # async def insert_one( data):
    #     result = data
    #     password = data['password']

    #     for key, value in data.items():
    #         print("key: ", key, " type: ", type(key))
    #         print("val: ", value, " type: ", type(value))

    #     result['password'] = hashlib.md5(password.encode()).hexdigest()

    #     await BaseModel.insert_one(result)
    

# await MidtermMark.insert_one(dict(student=student, mark=int(nota), midterm_nr=nr_atestare, status="processing"))
