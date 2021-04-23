# AIRecommenderSimilarPosts
Teza de licenta - AI system for recommending similar posts


To start mongo:
``` $ sudo systemctl start mongod```

## If problems with tensorflow/keras, use command:
``` $ pip install --user --upgrade tensorboard```

https://stackoverflow.com/questions/62465620/error-keras-requires-tensorflow-2-2-or-higher


## Example request to obtain an auth token from the app:
``` curl -iv -H "Content-Type: application/json" -d '{"username": "diana", "password": "mypassword"}' http://localhost:5005/api/auth```

## Example request to verify if token is valid:
```curl -iv -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjA2MmQwY2M5M2I5MTMwZjQ5YWMxZTJmIiwiZXhwIjoxNjE4NDk5OTE3fQ.kYHiAag027m_8JcRLDBPp2McPrMRD_JeImpzpn2-SWE" http://localhost:5005/api/auth/verify```



#### Useful resources and links
- https://github.com/mekicha/awesome-sanic
- https://its-a-feature.github.io/posts/2018/04/Creating-an-Apfell-Part-6/
- https://github.com/pyx/sanic-auth
- https://sanic-auth.readthedocs.io/en/latest/
- https://openbase.io/python/sanic-motor
- https://github.com/lixxu/sanic-motor
- https://www.vitoshacademy.com/hashing-passwords-in-python/
- https://pythonprogramming.net/password-hashing-flask-tutorial/
- 
