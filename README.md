# AIRecommenderSimilarPosts

## Description
This project proposes a solution based on Artificial Intelligence (including ML) algorithms to the problem of finding posts that contain images and text about lost or found pets which are similar in a time efficient way. The system does so by aggregating the similarity scores of the posts computed based on features extracted from images and texts. 

Although initially it was thought to use the system for finding similar posts of lost and found pets, the system can also be applied to other types of posts to detect their similarity and also recommend the top most similar posts.

For the ease of use, the system was embedded in a web platform which provides an API for external use.

For now, the system was implemented and tested to work with Romanian texts, but in the future it is planned to extend the system to other languages as well.

### Image similarity
![image similarity schema1](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/1image_schema1.png)

![image similarity schema2](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/2image_schema2.png)

### Text similarity

 ![text similarity schema](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/3text_schema3.png)
 
### Aggregated image+text posts similarity
![aggregated similarity schema](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/4aggregated_schema.png)

## Technologies used
- Python
- Keras
- Scikit-learn
- Pandas
- Nltk
- Sanic Web Framework
- Motor Driver for Mongo
- HTML, CSS, Bootstrap
- and others

## Screenshots

| | | 
|:-------------------------:|:-------------------------:
|<img width="1604" alt="screen shot 1" src="https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen1.png">  blah |  <img width="1604" alt="screen shot 2" src="https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen2.png">|
|<img width="1604" alt="screen shot 3" src="https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen3.png"> |  <img width="1604" alt="screen shot 4" src="https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen4.png">|


<!-- commented: -->
<!-- [screenshot1](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen1.png) -->
<!--![screenshot2](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen2.png) -->
<!--![screenshot3](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen3.png) -->
<!-- ![screenshot4](https://github.com/mdiannna/AIRecommenderSimilarPosts/blob/main/schemas_and_screenshots/screen4.png) -->

## How to run
``` $pip3 install -r requirements.txt ```

``` python3 app.py ```

## Technical details / how to run (in progress):
To start mongo:
``` $ sudo systemctl start mongod```

### If problems with tensorflow/keras, use command:
``` $ pip install --user --upgrade tensorboard```

https://stackoverflow.com/questions/62465620/error-keras-requires-tensorflow-2-2-or-higher


### Example request to obtain an auth token from the app:
``` curl -iv -H "Content-Type: application/json" -d '{"username": "diana", "password": "mypassword"}' http://localhost:5005/api/auth```

### Example request to verify if token is valid:
```curl -iv -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjA2MmQwY2M5M2I5MTMwZjQ5YWMxZTJmIiwiZXhwIjoxNjE4NDk5OTE3fQ.kYHiAag027m_8JcRLDBPp2McPrMRD_JeImpzpn2-SWE" http://localhost:5005/api/auth/verify```


### Example of GET request with curl (read post with id1)
curl -X GET -iv  -H "Content-Type: application/json"  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjA2MmQwY2M5M2I5MTMwZjQ5YWMxZTJmIiwiZXhwIjoxNjIwNDY0MTI0fQ.vA4GkrGAOX3OT0dW7d7FEsGy5Jm2DHUNZyTIAcN-HyY"  -d '{"post_id": "1"}'  http://localhost:5005/api/post/read



## Some useful resources and links
- https://github.com/mekicha/awesome-sanic
- https://its-a-feature.github.io/posts/2018/04/Creating-an-Apfell-Part-6/
- https://github.com/pyx/sanic-auth
- https://sanic-auth.readthedocs.io/en/latest/
- https://openbase.io/python/sanic-motor
- https://github.com/lixxu/sanic-motor
- https://www.vitoshacademy.com/hashing-passwords-in-python/
- https://pythonprogramming.net/password-hashing-flask-tutorial/
