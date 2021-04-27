# -*- coding: utf-8 -*-

from sanic.exceptions import abort
from sanic import Sanic
from sanic import response, request
from sanic_jinja2 import SanicJinja2
import os
from post import Post
from termcolor import colored
import time
import aiofiles
import pprint

import json
from similarity_aggregator import SimilarityAggregator
from sanic_session import InMemorySessionInterface
from sanic_jwt.decorators import protected

# https://sanic-auth.readthedocs.io/en/latest/
from sanic_auth import Auth
from sanic_motor import BaseModel
from models import User, Post
from utils import check_password, create_hash
from sanic_jwt import exceptions
from sanic_jwt import initialize

from TextExtractionRuleBased.rulebased import RuleBasedInformationExtractor
from ImageSimilarityModule.imagesimilarity import ImageSimilarity
from bson.json_util import dumps, loads
from bson import json_util
from utils import post_to_json
import numpy as np

app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.config.UPLOAD_FOLDER = 'images'



# settings = dict(MOTOR_URI='mongodb://db-mongo:27018/service2-mongo-students',
#                 LOGO=None)
settings = dict(MOTOR_URI='mongodb://localhost:27017/service2-mongo-students',
                LOGO=None)
app.config.update(settings)

BaseModel.init_app(app)

auth = Auth(app)


jinja = SanicJinja2(app, autoescape=True)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)


# change to false in production!
app.config['DEBUG'] = True

app.static('/static', './static')


# for debug of static files folder:
# print(colored("static", "red"))
# print(app.url_for('static', name='static', filename='css/theme1.css'))


imgSim = None
similarity = None

@app.listener('before_server_start')
async def setup_db(app, loop):
    global imgSim
    global similarity
    # init image similarity module class
    imgSim = ImageSimilarity() 
    # time.sleep(2)
    # TODO: fix problem of allocating ... for GPU twice
    similarity = SimilarityAggregator(image_module=imgSim)



# TODO: NOTE
# For demonstration purpose, use a mock-up globally-shared session object.
session = {}



@app.middleware('request')
async def add_session(request):
    request.ctx.session = session

# @app.middleware("request")
# async def add_session_to_request(request):
#     # before each request initialize a session
#     # using the client's request
#     await session.open(request)


# @app.middleware("response")
# async def save_session(request, response):
#     # after each request save the session,
#     # pass the response to set client cookies
#     await session.save(request, response)


@app.route('/')
async def index(request):
    return jinja.render("index.html", request)



@app.route('/json-hello')
async def index_json(request):
    """ route for testing, returns a json response"""
    return response.json("Hello!")

@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # fetch user from database
        user = await User.find_one({"name":username})

        print("user:", user)
        # user = some_datastore.get(name=username)
        if user and check_password(user.password, password):
            auth.login_user(request, user)
            # return response.redirect('/profile')
            return response.redirect('/dashboard')

    # return response.html(HTML_LOGIN_FORM)
    return jinja.render("login.html", request)


async def api_auth(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await User.find_one({"name":username})

    
    print("user:", user)
    # user = some_datastore.get(name=username)
    if user != None and check_password(user.password, password):
        #temporary solution:
        user_dict = {
            "user_id": str(user.id),
            "username": user.username,
            "password": user.password
        }
        # auth.login_user(request, user)
        return user_dict

    raise exceptions.AuthenticationFailed("Wrong username or password.")
    


@app.route('/register', methods=['GET', 'POST'])
async def register(request):
    message = ''
    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        confirm_password = request.form.get('confirm_password')

        print("username:", username)
        print("password:", password)
        print("confirm_passwrod:", confirm_password)
        # fetch user from database
        # user = await User.find_one({"name":username})

        print(dict(name=username, password=password))

        if password==confirm_password:
            await User.insert_one(dict(name=str(username), password=create_hash(password)))

            # TODO: if user inserted ... etc...
            return response.redirect('/dashboard')

    # return response.html(HTML_LOGIN_FORM)
    return jinja.render("register.html", request)


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route('/profile')
@auth.login_required(user_keyword='user')
async def profile(request, user):

    print(colored(user, "red"))

    return jinja.render("profile.html", request, user=user.name)

@app.route('/documentation')
async def documentation(request):
    return jinja.render("documentation.html", request)


# Method for testing get similar posts
@app.route('/demo-similar-posts', methods=['GET'])
async def demo_similar_posts(request):
    demo_token = await app.auth.generate_access_token(user={"user_id":-1, "username":"demo_user"})
    return jinja.render("demo_similar_posts_UI.html", request, greetings="Hello, sanic!", token=str(demo_token))

# Method for testing similar pairs of images
@app.route('/demo-similar-images', methods=['GET'])
async def demo_similar_images(request):
    demo_token = await app.auth.generate_access_token(user={"user_id":-1, "username":"demo_user"})
    return jinja.render("demo_similar_images.html", request, token=str(demo_token))

# Method for testing get similar images
@app.route('/demo-get-similar-images', methods=['GET'])
async def demo_get_similar_images(request):
    demo_token = await app.auth.generate_access_token(user={"user_id":-1, "username":"demo_user"})
    return jinja.render("demo_get_similar_images.html", request, token=str(demo_token))

# Method for testing Named Entity Recognition (NER)
@app.route('/demo-text-info-extractor', methods=['GET'])
async def demo_text_info_extractor(request):
    demo_token = await app.auth.generate_access_token(user={"user_id":-1, "username":"demo_user"})
    return jinja.render("demo_text_extraction.html", request, token=str(demo_token))

@app.route('/demo-ner', methods=['GET'])
async def demo_ner(request):
    demo_token = await app.auth.generate_access_token(user={"user_id":-1, "username":"demo_user"})
    return jinja.render("demo_ner.html", request, token=str(demo_token))


@app.route('/ner-annotator', methods=['GET'])
async def ner_annotator(request):
    text = "test test hello lalala"
    return jinja.render("ner_annotator.html", request, text=text)


# Method for testing add post api (delete later if needed )TODO
@app.route('/demo-add-post', methods=['GET'])
async def demo_add_post(request):
    demo_token = await app.auth.generate_access_token(user={"user_id":-1, "username":"demo_user"})
    return jinja.render("demo_add_post_api.html", request, greetings="Hello, sanic!", token=str(demo_token))


# TODO
@app.route('/dashboard', methods=['GET'])
@auth.login_required(user_keyword='user')
async def dashboard(request, user):
    return jinja.render("dashboard.html", request, user=user.name)


@protected()
@app.route('/api/post/create', methods=['POST'])
async def make_post(request):
    #TODO: save & retrieve token of the user
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

    print("request args:", request.args)
    print("request form:", request.form)

    # if not 'post_id' in request.args:
    if not 'post_id' in request.form:
        return response.json({"status":"error", "message":'Must include the "post_id" as a parameter in request!'}, status=400)

    # if not 'text' in request.args:
    if not 'text' in request.form:
        return response.json({"status":"error", "message":'Must include the "text" as a parameter in request!'}, status=400)

    post_id_external = request.form['post_id'][0]
    post_text = request.form['text'][0]
    
    username = "user1" #TODO: get this from token request!!! 
    user_id = "1" #TODO: get this from token request!!!

    fields = {}    
    if 'fields' in request.args:
        fields = request.args['fields']

    #upload image    
    if 'image' not in request.files:
        return response.json({"status":"error", "message":"no files for image"}, status=400)

    # useful resource: https://stackoverflow.com/questions/48930245/how-to-perform-file-upload-in-sanic
    upload_folder_name = app.config.UPLOAD_FOLDER

    if not os.path.exists(upload_folder_name):
        os.makedirs(upload_folder_name)

    print("upload_folder_name:", upload_folder_name)
    if upload_folder_name[-1]!="/":
        upload_folder_name += "/"

    upload_folder_name += username + "/"

    if not os.path.exists(upload_folder_name):
        os.makedirs(upload_folder_name)

    img_path = upload_folder_name+request.files["image"][0].name

    async with aiofiles.open(upload_folder_name+request.files["image"][0].name, 'wb') as f:
        await f.write(request.files["image"][0].body)

    imgFeatures = imgSim.extract_features(model='default', img_path=img_path)

    await Post.insert_one(dict(
        post_id_external=str(post_id_external),
        user_id='user' + user_id,
        img_path=img_path,
        text=post_text,
        fields=fields, #TODO:later check,
        img_features=imgFeatures.tolist()
        ))

    #TODO: try catch for errors
    return response.json({"status":"success", "message": "post succesfully created"})



# Method for testing viewing all posts, TODO: delete later!!!
@app.route('/all-posts', methods=['GET'])
async def view_all_posts(request):

    # await Post.delete_many({}) #works as drop

    n = await Post.count_documents({})
    print('%s posts in collection' % n)

    posts_cursor = await Post.find(sort='user_id')
    json_data = []
    
    results = []
    for obj in posts_cursor.objects:
        # print(type(obj))
        # print(obj)
        
        results.append(post_to_json(obj))

    #     obj.pop('_id')
    #     # if obj.student == student:
    #     # results.append(obj.text)
    #     # posts.append(obj.user_id)
    #     # results.append(obj.text)
    #     results.append(obj)

    # posts = results

    #TODO:!!! fix problem & get posts!!!
  
    # marks = cursor_marks.objects
    # results = []
    # for obj in marks:
    #     if obj.student == student:
    #         results.append(int(obj.mark))

    # posts = []
    # for post in posts_cursor.to_list(length=100):
    #     pprint.pprint(post)
    #     post.pop('_id')
    #     posts.append(post)

    # return response.json({"TODO":"TODO: Delete this route later!!!", "posts": posts, "results":results})
    return response.json({"TODO":"TODO: Delete this route later!!!", "posts": results})


#TODO!!!!!!!!!! test & finish
# TODO: verificat daca nu trebuie sa fie sincron! si daca nu trebuie post!
# TODO: need to be authorized from API
@protected()
@app.route('/api/get-similar-posts', methods=['POST'])
async def get_similar_posts(request):
    """ 
    Get n similar posts to the post (image and text) included in request, returns n similar posts
    The arguments should be "post_image", "post_text" and "max_similar" (optional).
    If not included in request, max_similar is by default 3
    """

    if not 'post_image' in request.args:
        return response.json({"status":"error", "message":'Must include the "post_image" as a parameter in request!'}, status=400)
        # return abort(400, 'Must include the "post_image" as a parameter in request!') refactored
    
    if not 'post_text' in request.args:
        return response.json({"status":"error", "message":'Must include the "post_text" as a parameter in request!'}, status=400)
        # return abort(400, 'Must include the "post_text" as a parameter in request!')
    
    post_img = request.args['post_image']
    post_txt = request.args['post_text']

    # post = Post(post_img, post_txt)
    
    max_similar = 3 # default 3 similar posts maximum

    if 'max_similar' in request.args:
        max_similar = request.args['max_similar']
    
    # TODO
    try:
        # result = similarity.get_similar_posts(post, n)
        result = similarity.get_similar_posts(post_img, post_txt, max_similar)

        return response.json(result)
    except Exception as e:
        # TODO: log somewhere
        # return abort(500, str(e)) refactored
        print("Error: " + str(e))
        return response.json({"status":"error", "message":str(e)}, status=500)
        

    return response.json("TODO: make post and save to db")


# Exemplu de post request:
#curl -X POST  -H "Content-Type: application/json" \
# -d 'text=S-a perdut in com.Tohatin, caine de rasa ,,BEAGLE,,, mascul pe nume ,,KAY,,Va rugam frumos sa ne anuntati daca stiti ceva informatie despre prietenul familie&token=tobedefined' http://0.0.0.0:5005/api/text-extract
# TODO: need to be authorized from API - check real token!
# TODO: remove GET method after testing!
@app.route('/api/text-extract', methods=['POST'])
@protected()
async def simple_text_extract(request):
    params = []
    if request.form:
        type_request = "FORM"
        params = request.form
        print(colored("form:","yellow"), request.form)
    elif request.json:
        params = request.json
        type_request = "JSON"
        print(colored("json:", "yellow"), request.json)
    else:
        return response.json({"status":"error", "message":"missing parameter text in request (request type should be json or multipart/form-data)"}, status=400)

    if not ("text" in params):
        return response.json({"status":"error", "message":"missing parameter text in request"}, status=400)
    try:
        text = str(params["text"][0])
        # print("text:", text)
    except:
        return response.json({"status":"error", "message":"text parameter has wrong format"}, status=400)

    extractor = RuleBasedInformationExtractor()
    
    # TODO: add logs if needed
    try:
        result =  extractor.extract_fidels_from_config(text, 'TextExtractionRuleBased/configurations/config.xml', verbose=False)
        # result =  extractor.extract_fidels_from_config(text, 'TextExtractionRuleBased/configurations/config.xml', verbose=True)

        # for debug: log it & delete it!
        # print(colored("Extracted from config file:", "blue"), result)

        if result[1]=="success":
            return response.json({"status":"success", "result": result, "message":""})
        else:
            print("Error: " + str(result))
            return response.json({"status":"error", "message":"Errors in Config file for Rule-Based Text Extractor!", "result": []}, status=500)
    except Exception as e:
        print("Error: " + str(e))
        return response.json({"status":"error", "message":"Something went wrong with fields extraction from config file!", "result": []}, status=500)

    return response.json({"status":"error", "message":"Something went wrong with fields extraction from config file!", "result": []}, status=500)



def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/api/image-pairs-similarity", methods=['POST'])
@protected()
async def get_img_pairs_similarity(request):
    params = []
    
    if request.form:
        type_request = "FORM"
        params = request.form
        print(colored("form:","yellow"), request.form)
    elif request.json:
        params = request.json
        type_request = "JSON"
        print(colored("json:", "yellow"), request.json)
    else:
        return response.json({"status":"error", "message":"missing parameters img1 and img2 in request (request type should be json or multipart/form-data)"}, status=400)


    # TODO: check
    # allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}


    if request.method == 'POST':
        # check if the post request has the file part
        if 'img1' not in request.files or 'img2' not in request.files:
            return response.json({"status":"error", "message":"no files for image1 and image2"}, status=400)
            # flash('No file part')
            # return redirect(request.url)

        # file = request.files['img1']  
        # print("file:", file)

        # useful resource: https://stackoverflow.com/questions/48930245/how-to-perform-file-upload-in-sanic
        upload_folder_name = app.config.UPLOAD_FOLDER
        if not os.path.exists(upload_folder_name):
            os.makedirs(upload_folder_name)


        print("upload_folder_name:", upload_folder_name)
        if upload_folder_name[-1]!="/":
            upload_folder_name += "/"

        #add for demo user
        upload_folder_name += "demo_user/demo/"

        img_path1 = upload_folder_name+request.files["img1"][0].name

        async with aiofiles.open(upload_folder_name+request.files["img1"][0].name, 'wb') as f:
            await f.write(request.files["img1"][0].body)

        img_path2 = upload_folder_name+request.files["img2"][0].name

        async with aiofiles.open(img_path2, 'wb') as f:
            await f.write(request.files["img2"][0].body)
        

        print("img path1:", img_path1)
        print("img path2:", img_path2)


        # TODO:make async!!
        similarity_score = imgSim.calc_similarity(img_path1, img_path2)
        print("similarity score:", similarity_score)

        if similarity_score and similarity_score>0:
            return response.json({"status":"success", "similarity_score": str(similarity_score)})
            # TODO
        #     # if user does not select file, browser also
        #     # submit an empty part without filename
        #     if file.filename == '':
        #         flash('No selected file')
        #         return redirect(request.url)
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #         return redirect(url_for('uploaded_file',
        #                                 filename=filename))
        # # return 



    return response.json("TODO: compute similarity & return")


@protected()
@app.route('/api/get-similar-images', methods=['POST'])
# @app.route('/api/get-similar-images')
async def get_similar_images(request):
    """ 
    Get n similar image to image included in request, returns n similar images
    The arguments should be "post_image" and "max_similar" (optional).
    include_paths is opt parameters to return image paths for frontend as well
    If not included in request, max_similar is by default 3
    """

    if request.form:
        type_request = "FORM"
        params = request.form   
        print(colored("form:","yellow"), request.form)
    elif request.json:
        params = request.json
        type_request = "JSON"
        print(colored("json:", "yellow"), request.json)
    else:
        return response.json({"status":"error", "message":"missing parameters request (request type should be json or multipart/form-data)"}, status=400)

    max_similar = 3
    if 'max_similar' in params:
        try:
            max_similar = int(params['max_similar'][0])
        except:
            print("max_similar param wrong, setting as default to 3") #TODO: add in response
            max_similar = 3
        
    if 'image' not in request.files:
        return response.json({"status":"error", "message":"missing 'image' file"}, status=400)
    
    upload_folder_name = app.config.UPLOAD_FOLDER
        
    if not os.path.exists(upload_folder_name):
        os.makedirs(upload_folder_name)

    print("upload_folder_name:", upload_folder_name)
    if upload_folder_name[-1]!="/":
        upload_folder_name += "/"

    #TODO!!! get user from token from request!!!
    username = 'user1'
    upload_folder_name += username + "/"

    if not os.path.exists(upload_folder_name):
        os.makedirs(upload_folder_name)

    img_path = upload_folder_name+request.files["image"][0].name

    async with aiofiles.open(img_path, 'wb') as f:
        await f.write(request.files["image"][0].body)

    imgFeatures = imgSim.extract_features(model='default', img_path=img_path)
    
    print("img features:", imgFeatures)

    filter = {"user_id":"user1"}
    # posts_cursor = await Post.find({"user_id":username}) #TODO: get only for the user!!!!
    # posts_cursor = await Post.find(filter=filter, limit=10) #TODO: get only for the user!!!!
    posts_cursor = await Post.find(filter=filter, limit=1000) #TODO: get only for the user!!!!
    json_data = []
    
    # results = []
    all_imgs_features = {}

    for obj in posts_cursor.objects:
        data = obj.img_features
        all_imgs_features[str(obj.id)] =  np.array(data)


    similarities = imgSim.get_similar_img_by_features(imgFeatures, all_imgs_features, max_similar_imgs=max_similar)
    
    if 'include_paths' in params:
        image_paths_map = {"img_id":"img_path TODO"}
        # TODO: check for errors
        return response.json({"status":"success", "results":similarities, "img_paths_map":image_paths_map})
    
    # TODO: check for errors    
    return response.json({"status":"success", "results":similarities})



### Test route for api, can be accessed only with a valid acces_token
# example request:
# curl localhost:5005/api/test-iv -H "Authorization: Bearer eyJ0eXAiOiJKg02E" http:/localhost:5005/api/test-api
@app.route("/api/test-api", methods=['POST', 'GET'])
@protected() #can access route only with valid token
def test_api_auth(request):
  return response.json("Hello!")


initialize(app, authenticate=api_auth, url_prefix='/api/auth', path_to_retrieve_user='/me')
# https://sanic-jwt.readthedocs.io/en/latest/pages/endpoints.html
# initialize(
#     app,
#     url_prefix='/api/auth'
#     path_to_authenticate='/my_authenticate',
#     path_to_retrieve_user='/my_retrieve_user',
#     path_to_verify='/my_verify', # => localhost:5000/api/auth/my_v
#     path_to_refresh='/my_refresh',
# )


if __name__ == '__main__':
    port = os.environ.get("SERVER_PORT", 5005)
    host = os.environ.get("SERVER_HOST", '0.0.0.0')

    app.run(host=host, debug=True, port=port)
