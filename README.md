# ImageUpAPI
<div id="top"></div>

Django Rest Framework application that allows user to upload image in PNG or JPG format and then 
accordingly to user's account tier get links to generated thumbnails and original image. If user's account tier allows it, expiring link to the image can be generated with expiring time set between 300 and 30000 seconds.
The app provides DRF UI. 

## Technologies Used
* Python 3.11
* Django 4.2.6
* RabbitMQ
* Celery 5.3.4
* Django REST 3.14
* PostgreSQL 14.9
* docker-compose

## Features Implemented
- users can upload images via HTTP request
- users can list their images
- three builtin `account tiers Basic, Premium and Enterprise`
  - users that have a `"Basic"` plan after uploading an image get: 
    - a link to a thumbnail that's 200px in height
  - users that have a `"Premium"` plan get:
    - a link to a thumbnail that's 200px in height
    - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
  - users that have a `"Enterprise"` plan get
    - a link to a thumbnail that's 200px in height
    - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
    - ability to fetch an expiring link to the image (the link expires after a given number of seconds 
    (the user can specify any number between 300 and 30000))
- apart from the builtin tiers, admins can create arbitrary tiers with the following things configurable:
  - `arbitrary thumbnail sizes`
  - `presence of the link to the originally uploaded file`
  - `ability to generate expiring links`
- admin UI has been done via django-admin
- tests for image upload, thumbnail generation, expiring link creation, 
built-in account tiers permissions, custom account tiers permissions
- `performance considerations`(implemented basic task queue to be able to process a lot of images)

## Local Setup

- clone the repository
- cd to main folder
- run `docker-compose up -d --build` (the startup database is created with three built-in account tiers
and admin superuser with default credentials `admin:admin`)
- Admin page url - `http://localhost:8000/admin/` or `http://127.0.0.1:8000/admin/`
- users can be created via admin panel
- login can be done via django rest framework UI or http://127.0.0.1:8000/api-auth/login/?next=/

Authenticated users

- http://127.0.0.1:8000/ - list of images
- http://127.0.0.1:8000/upload/ - for upload image
- http://127.0.0.1:8000/expiring-link/ - for creating expiring link to an image 
(Enterprise user or custom tier user with this feature allowed)


<br />
<p align="right">(<a href="#top">back to top</a>)</p>
