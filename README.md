# Digitize invoices
This project is used to digitize the invoices uploaded by the user

## User page
![](https://i.imgur.com/yi4pBmh.png)

## Admin page
![](https://i.imgur.com/KOwPhMw.png)


### User flow
#### steps:
1. create user by providing role user/admin (please note username and password for further purpose)
2. update invoice in user page
    - After uploading file, page will get refreshed and show the user about their digitization status with download and view link
    - **Note** : you will not able to find the view link in info column until the invoice has been digitized.
3. Logout from user page and login as admin from the navigation bar by clicking on user icon and then logout.
4. Here you will see all the invoices uploaded by all users where you can download and update the invoice status by clicking on download/update link.
5. In update page you can give details like invoice_no, from, to, date and save or you can digitize there itself then page get reloaded with the updated info
    - If admin would have pressed on digitize button he/she may not see the update button in admin home page as well as view page.
  
  
### Other UI pages
##### SignUp Page
![](https://i.imgur.com/8YECDTu.png)
  
##### SignIn page
![](https://i.imgur.com/2Pbw8LP.png)

##### view/update page to digitize
![](https://i.imgur.com/iglyHcW.png)
- Once the admin digitize the invoice he/she would not be able to update any value.
![](https://i.imgur.com/9ruPjrF.png)



## Stack details
```bash
Framework : python-Django
version : Django-2.2

Database:
Db : sqlite (default)

Backend:
Language : python
verison : python3

Front-end:
HTML : HTML5
css : bootstrap4
js

Hostname:
host : localhost (default)
```

## Installation
```bash
git clone https://github.com/goutham9032/digitize_invoices.git
cd digitize_invoices
```

```bash
pip3 install -r requirements.txt
```

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```

```bash
python3 manage.py runserver 0:2222 
```
> Note: when you want to run this application on server, please add domain name/ip address in ALLOWEDHOSTS in settings.py

## In browser
```python
http://localhost:2222 
     or
http://<ipaddress/domain name>:2222 # when you are running on server
```
