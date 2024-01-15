# [PMA-API]
Django API to manage Roles during Prosit sessions.

<br />
> Features:

- ✅ `Up-to-date Dependencies`

- ✅ `User's registration`

- ✅ `Prosit Browsing`

- ✅ `Prosit' Roles Management`

- ✅ `Prosit Reports Generation`

<br />

## Manual Build
> Download the code
```bash
$ git clone https://github.com/CamCoder337/pma-api.git
$ cd pma-api
```
<br />

> Setup for 'Unix', 'MacOs' > Install modules via 'env'
```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
<br />

> Setting up .env files
<br />
Set them up according to your needs (Check the sample) 🙂

<br />

> Set Up Database
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
<br />

> Start the API Server
```bash
$ python manage.py runserver 5000     # start api
```

Use the API via `POSTMAN` or `Swagger Dashboard` at `localhost:5000`.

<br />

### [PMA-API] - provided **[Camcoder337](https://ftdev.me/)**.