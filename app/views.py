# Python imports
import time
import json
import re

# Django imports
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage

# user defined imports
from app.models import Invoice, AddParsedInfo

def register(request):
    '''
    This function will open signup page and take required user info and create user in database and 
    redirects to users home page
    '''
    if request.method == 'POST':
        post_body = request.POST.dict()
        username, email = post_body['username'], post_body['email']
        firstname, lastname = post_body['firstname'], post_body['lastname']
        password, role = post_body['password'], post_body['role']
        user_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        if not (user_exists or email_exists):
            User.objects.create_user(username=username, email=email,
                                     password=password, first_name=firstname,
                                     last_name=lastname, is_superuser=True if role=='admin' else False)
            user = authenticate(username = username, password = password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = dict(success=False, user_exists=user_exists, email_exits=email_exists, data=post_body)
            return render(request, 'registration/register.html', context)
    return render(request, 'registration/register.html', {'success':True})

def login_user(request):
    '''
    This function will opens login page and authenticate user based on login details 
    '''
    if request.method == 'POST':
        req = request.POST.dict()
        username = req.get('username','')
        password = req.get('password','')
        if not (User.objects.filter(username=username).exists() and password):
            return render(request, 'registration/login.html', {'success': False, 'data':req})
        user = authenticate(username = username, password = password)
        if user and not user.useraddinfo.active:
           return render(request, 'registration/login.html', {'disabled': True,'data':req, 'success':True})
        if not user:
            return render(request, 'registration/login.html', {'success': False, 'data':req})
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'registration/login.html', {'success': True})

def logout_user(request):
    '''
    This function will logout user 
    '''
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    if request.method == "GET":
       if request.user.is_superuser:
          invoices = Invoice.objects.all()
       else:
          invoices = Invoice.objects.filter(owner=request.user)
       return render(request, "home.html", {'invoices': invoices})
    if request.method == 'POST' and 'input_file' in request.FILES:
       file_obj = request.FILES["input_file"]
       fs = FileSystemStorage()
       file_name = re.sub("[^a-zA-Z0-9\n\.]", "-", file_obj.name)
       current_ts = int(time.time())
       file_id = "%s_%s" % (current_ts, file_name)
       filename = fs.save(file_id, file_obj)
       file_location = fs.url(filename)
       Invoice.objects.create(slug=current_ts, file_name=file_id, owner=request.user, download_url=file_location)
       return JsonResponse({"success": True })

@csrf_exempt
@login_required
def view_update_invoice(request, invoice_id):
    invoice_obj = Invoice.objects.filter(slug=invoice_id) 
    if request.method != 'POST':
       if invoice_obj.exists():
          invoice = AddParsedInfo.objects.filter(invoice=invoice_obj.first())
          return render(request, "invoice_view_edit.html", {'invoice':invoice.first(), 'data':invoice_obj.first()})
       else:
          return render(request, "invoice_view_edit.html", {'data':invoice_obj.first()})
    body = json.loads(request.body.decode())
    if invoice_obj:
       add_info = AddParsedInfo.objects.filter(invoice=invoice_obj.first())
       if add_info.exists():
          add_info.update(from_add=body['from'], invoice_no=body['invoice_no'], 
                          to=body['to'], date=body['date'])
       else:
          AddParsedInfo.objects.create(invoice=invoice_obj.first(), from_add=body['from'], 
                                       invoice_no=body['invoice_no'], to=body['to'], date=body['date'])
       return JsonResponse({"success": True })
    else:
       pass

@csrf_exempt
@login_required
def digitize_invoice(request, invoice_id):
    invoice_obj = Invoice.objects.filter(slug=invoice_id)
    if invoice_obj.exists():
       invoice_obj.update(digitized=True)
       return JsonResponse({"success": True })
    else:
       return JsonResponse({"success": False })
    
