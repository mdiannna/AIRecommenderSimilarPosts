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

app = Sanic(__name__)

jinja = SanicJinja2(app, autoescape=True)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)

similarity = SimilarityAggregator()

# change to false in production!
app.config['DEBUG'] = True
app.static('/static', './static')
# app.static('/static/css', './static/css')
# app.static('/static/js', './static/js')

print(colored("static", "red"))
print(app.url_for('static', name='static', filename='css/theme.css'))

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
@app.route('/demo-ner', methods=['GET'])
async def demo_ner(request):
    return jinja.render("demo_ner.html", request)


# TODO
@app.route('/dashboard', methods=['GET'])
async def dashboard(request):
    return jinja.render("dashboard.html", request)


@app.route('/make-post', methods=['POST'])
async def make_post(request):
    return response.json("TODO: make post and save to db")


# TODO: verificat daca nu trebuie sa fie sincrona! si daca nu trebuie post!
@app.route('/request-similar-posts', methods=['POST'])
async def request_similar_posts(request):
    """ 
    Get n similar posts to the post (image and text) included in request, returns n similar posts
    The arguments should be "post_image", "post_text" and "n" (optional).
    If not included in request, n is by default 3
    """

    if not 'post_image' in request.args:
        return abort(400, 'Mush include the "post_image" as a parameter in request!')
    
    if not 'post_text' in request.args:
        return abort(400, 'Mush include the "post_text" as a parameter in request!')
    
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
        return abort(500, str(e))

    return response.json("TODO: make post and save to db")


if __name__ == '__main__':
    port = os.environ.get("SERVER_PORT", 5005)
    host = os.environ.get("SERVER_HOST", '0.0.0.0')

    app.run(host=host, debug=True, port=port)
