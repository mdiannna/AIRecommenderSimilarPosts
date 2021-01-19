# -*- coding: utf-8 -*-

from sanic.exceptions import abort
from sanic import Sanic
from sanic import response, request
from sanic_jinja2 import SanicJinja2
import os
from post import Post
from termcolor import colored

from similarity_aggregator import SimilarityAggregator
from sanic_session import InMemorySessionInterface

# https://sanic-auth.readthedocs.io/en/latest/
from sanic_auth import Auth
from sanic_motor import BaseModel
from models import User
from utils import check_password, create_hash
from TextExtractionRuleBased.rulebased import RuleBasedInformationExtractor

app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'

# settings = dict(MOTOR_URI='mongodb://db-mongo:27018/service2-mongo-students',
#                 LOGO=None)
settings = dict(MOTOR_URI='mongodb://localhost:27017/service2-mongo-students',
                LOGO=None)
app.config.update(settings)

BaseModel.init_app(app)

auth = Auth(app)

jinja = SanicJinja2(app, autoescape=True)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)

similarity = SimilarityAggregator()

# change to false in production!
app.config['DEBUG'] = True

app.static('/static', './static')

# for debug of static files folder:
# print(colored("static", "red"))
# print(app.url_for('static', name='static', filename='css/theme1.css'))


# NOTE
# For demonstration purpose, we use a mock-up globally-shared session object.
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
    return jinja.render("demo_similar_posts_UI.html", request, greetings="Hello, sanic!")

# Method for testing get similar images
@app.route('/demo-similar-images', methods=['GET'])
async def demo_similar_images(request):
    return jinja.render("demo_similar_images.html", request)

# Method for testing Named Entity Recognition (NER)
@app.route('/demo-text-info-extractor', methods=['GET'])
async def demo_text_info_extractor(request):
    return jinja.render("demo_text_extraction.html", request)

@app.route('/demo-ner', methods=['GET'])
async def demo_ner(request):
    return jinja.render("demo_ner.html", request)


@app.route('/ner-annotator', methods=['GET'])
async def ner_annotator(request):
    text = "test test hello lalala"
    return jinja.render("ner_annotator.html", request, text=text)


# TODO
@app.route('/dashboard', methods=['GET'])
@auth.login_required(user_keyword='user')
async def dashboard(request, user):
    return jinja.render("dashboard.html", request, user=user.name)


# TODO: need to be authorized from API
@app.route('/make-post', methods=['POST'])
async def make_post(request):
    return response.json("TODO: make post and save to db")


# TODO: verificat daca nu trebuie sa fie sincrona! si daca nu trebuie post!
# TODO: need to be authorized from API
@app.route('/request-similar-posts', methods=['POST'])
async def request_similar_posts(request):
    """ 
    Get n similar posts to the post (image and text) included in request, returns n similar posts
    The arguments should be "post_image", "post_text" and "n" (optional).
    If not included in request, n is by default 3
    """

    if not 'post_image' in request.args:
        return response.json({"status":"error", "message":'Must include the "post_image" as a parameter in request!'}, status=400)
        # return abort(400, 'Must include the "post_image" as a parameter in request!') refactored
    
    if not 'post_text' in request.args:
        return response.json({"status":"error", "message":'Must include the "post_text" as a parameter in request!'}, status=400)
        # return abort(400, 'Must include the "post_text" as a parameter in request!')
    
    post_img = request.args['post_image']
    post_txt = request.args['post_text']

    post = Post(post_img, post_txt)
    
    n = 3 # default 3 posts

    if 'n' in request.args:
        n = request.args['n']
    
    # TODO
    try:
        result = similarity.get_similar_posts(post, n)
        return response.json(result)
    except Exception as e:
        # TODO: log somewhere
        # return abort(500, str(e)) refactored
        return response.json({"status":"error", "message":str(e)}, status=500)
        

    return response.json("TODO: make post and save to db")



# Exemplu de post request:
#curl -X POST  -H "Content-Type: application/json" \
# -d 'text=S-a perdut in com.Tohatin, caine de rasa ,,BEAGLE,,, mascul pe nume ,,KAY,,Va rugam frumos sa ne anuntati daca stiti ceva informatie despre prietenul familie&token=tobedefined' http://0.0.0.0:5005/api/text-extract
# TODO: need to be authorized from API - check real token!
# TODO: remove GET method after testing!
@app.route('/api/text-extract', methods=['POST', 'GET'])
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
        return response.json({"status":"error", "message":"missing parameters text and token in request (request type should be json or multipart/form-data)"}, status=400)

    # TODO: check if token is correct - AUTH
    if not("token" in params and "text" in params):
        return response.json({"status":"error", "message":"missing parameters text or token in request"}, status=400)

    try:
        text = str(params["text"])
    except:
        return response.json({"status":"error", "message":"text parameter has wrong format"}, status=400)

    extractor = RuleBasedInformationExtractor()
    
    # TODO: add logs if needed
    try:
        result =  extractor.extract_fidels_from_config(text, 'TextExtractionRuleBased/configurations/config.xml', verbose=False)
        # for debug: log it & delete it!
        # print(colored("Extracted from config file:", "blue"), result)

        if result[1]=="success":
            return response.json({"status":"success", "result": result, "message":""})
        else:
            return response.json({"status":"error", "message":"Errors in Config file for Rule-Based Text Extractor!", "result": []}, status=500)
    except:
        return response.json({"status":"error", "message":"Something went wrong with fields extraction from config file!", "result": []}, status=500)

    return response.json({"status":"error", "message":"Something went wrong with fields extraction from config file!", "result": []}, status=500)
    


if __name__ == '__main__':
    port = os.environ.get("SERVER_PORT", 5005)
    host = os.environ.get("SERVER_HOST", '0.0.0.0')

    app.run(host=host, debug=True, port=port)
