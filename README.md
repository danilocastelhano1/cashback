# Cashback in Django Rest Framework


## Steps
- run ```docker-compose up --build```
  (I used docker, because it's easy to test from your behalf)
Once the docker is running, you can test the API below


### I'm sending an export of requests from postman, file:
```Mais Todos.postman_collection.json```
just import to your postman and test API

I'm using basic auth for this assessment, also i added this inside settings.py
(is not recomended, but it's just a test, right?)
username = admin
password = mystrongpassword

feel free to create another user, using ```createsuperuser``` command inside docker


## Added Test Cases with APITestCase
just run inside docker:
```docker-compose run api bash```
then:
```python manage.py test```