from sanic_motor import BaseModel

class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['name', 'password']     
    

# example of Post:
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
class Post(BaseModel):
    __coll__ = 'posts'
    # __unique_fields__ = ['img_path', 'text', 'fields', 'img_features']     
