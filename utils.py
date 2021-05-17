import hashlib
import pandas as pd
import uuid

def create_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_password(real_password_hash, tested_password):
    hashed_test = create_hash(tested_password)

    if real_password_hash == hashed_test:
        return True

    return False


 # {
    # '_id': "1242345345",
    # 'post_id_external': "12", #should restrict: for a user_id post_id_external should be unique
    # 'user_id': "1231234",
    # 'img_path': "test.img",  # will be included in images/user_id/
    # 'text': "S-a pierdut caine de rasa ....", 
    # 'fields': {
    #     "rasa_caine": "beagle",
    #     "locatie": "Chisinau" 
    # }, 
    # 'img_features': "[134, 23234, 3423.44, 3243.33]" # array of floats saved as str
    # }

def post_to_json(post_item):
    result = {}

    result['id'] = str(post_item.id)
    result['post_id_external'] = post_item.post_id_external
    result['user_id'] = post_item.user_id
    result['img_path'] = post_item.img_path
    result['text'] = post_item.text
    result['fields'] = post_item.fields

    if post_item.fields_external:
        print("external fields:", post_item.fields_external)

    if post_item.fields_external:
        result['fields_external'] = post_item.fields_external

    result['img_features'] = post_item.img_features




    return result

# # TODO: later all fields, not hard-coded
def post_to_df(post_item)   :
    # post_item =  {
    #     '_id': "1242345345",
    #     'post_id_external': "12", #should restrict: for a user_id post_id_external should be unique
    #     'user_id': "1231234",
    #     'img_path': "test.img",  # will be included in images/user_id/
    #     'text': "S-a pierdut caine de rasa ....", 
    #     'fields': {
    #         "rasa_caine": "beagle",
    #         "locatie": "Chisinau" 
    #     }, 
    #     'img_features': "[134, 23234, 3423.44, 3243.33]" # array of floats saved as str
    #     }

    result = {}

    data = {
        'id': str(post_item.id),
        'post_id_external': post_item.post_id_external,
        'user_id': post_item.user_id,
        'img_path': post_item.img_path,
        'text': post_item.text,
        'fields': post_item.fields,
        'fields_external':post_item.fields_external,
        'img_features': post_item.img_features
    }

    print("data:", data)
    print("cols:", list(data.keys()))


    # df = pd.DataFrame.from_records([data], columns=list(data.keys()), index=[str(post_item.id)])
    df = pd.DataFrame([data], columns=list(data.keys()), index=[str(post_item.id)])
    print("df:", df.head())
    
    return df



def user_to_json(item):
    result = {}
    result['id'] = str(item.id)

    # result['username'] = item.name #TODO: decis trebuie sau nu/?
    result['name'] = item.name
    result['password'] = str(len(item.password)) + " characters [hidden]"



    return result


def create_unique_filename():
    return str(uuid.uuid4())
