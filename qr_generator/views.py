# account/views.py
import base64
from smtplib import SMTPServerDisconnected
from wsgiref.simple_server import WSGIRequestHandler
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings

from django.core.mail import send_mail
from django.contrib import messages

from .forms import ContactUsForm 
from PIL import Image
from django.conf import settings
from qr_gen_project.settings import  MEDIA_ROOT
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# --------------------imports

from django.shortcuts import render
from django.conf import settings
from qrcode import *
from .models import QRCollection, UserCollection


import mimetypes
import os
from django.http.response import HttpResponse
from django.shortcuts import render

User = get_user_model()


@login_required(login_url="/qr-gen/accounts/login")
def dashboard(request):
    template = 'qr_generator/dashboard/active_qr.html'
    context = {}

    try:
        user_ = UserCollection.objects.filter(qr_user=request.user)
        qr_code = [qr.qr_code for qr in user_]
        user_items = []

        # fetch the QR from QRcollections and append to the list
        [user_items.append(QRCollection.objects.get(id=qr)) for qr in qr_code]
        context['user_items'] = user_items
    
    except QRCollection.DoesNotExist as ex:
        messages.info(request, "No collection available")


    return render(request, template, context)


def index(request):
    context = {}
    return render(request, 'qr_generator/index.html', context)



def share_qr(request, pk):
    return render(request, 'qr_generator/share_qr.html', {'qr_image':pk})

# =========== CONVERT QR FORMATS ================

# Convert to JPEG
def convert_to_jpeg(path):
    image = Image.open(path)
    rgb_image = image.convert('RGB')
    jpeg_image = rgb_image.save(path.replace('.png', '.jpeg'), 'JPEG')
    return path.replace('.png', '.jpeg'), os.path.basename(path.replace('.png', '.jpeg'))

def convert_to_png(path):
    image = Image.open(path)
    rgb_image = image.convert('RGB')
    png_image = rgb_image.save(path.replace('.png', '.png'), 'PNG')
    return path.replace('.png', '.png'), os.path.basename(path.replace('.png', '.png'))

# Convert to JPG
def convert_to_jpg(path):
    image = Image.open(path)
    rgb_image = image.convert('RGB')
    jpg_image = rgb_image.save(path.replace('.png', '.jpg'), 'JPG')
    return path.replace('.png', '.jpg'), os.path.basename(path.replace('.png', '.jpg'))


# Convert to SVG
def convert_to_svg(path):
    startSvgTag = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    width="240px" height="240px" viewBox="0 0 240 240">"""
    endSvgTag = """</svg>"""
    pngFile = open(path, 'rb')
    base64data = base64.b64encode(pngFile.read())
    base64String = '<image xlink:href="data:image/png;base64,{0}" width="240" height="240" x="0" y="0" />'.format(base64data.decode('utf-8'))
    f = open(path.replace('.png', '.svg'), 'w')
    f.write(startSvgTag + base64String + endSvgTag)
    f.close()
    return path.replace('.png', '.svg'), os.path.basename(path.replace('.png', '.svg'))


# Convert to PDF
def convert_to_pdf(path):
    image = Image.open(path)
    rgb_image = image.convert('RGB')
    pdf_image = rgb_image.save(path.replace('.png', '.pdf'), 'PDF')
    return path.replace('.png', '.pdf'), os.path.basename(path.replace('.png', '.pdf'))

# =========== ENDCONVERT QR FORMATS ================


def qr_creator(request:WSGIRequestHandler, user: User, categ_: str) -> QRCollection:
    """This is the Main QR Creator Function:
        It creates the QR code and returns the created QR object
    """

    QRCollection.objects.create(
            qr_user = user,
            category = categ_.upper(),
            qr_info = 'Your {0} is: {1}.'.format(categ_.title(), request.POST[categ_])
            )

    created_qr_object = QRCollection.objects.filter(qr_user=user).order_by('-id')[0]

    return created_qr_object


@login_required(login_url="/qr-gen/accounts/login")
def generate_qr(request):
    """The Generte QR function accepts a WSGIRequest, if it's a POST request,
    it checks the name in the submitted form and uses the qr_creator function to process it """
    
    context = {}
    template = 'qr_generator/generateqr.html'
    
    if request.method == 'POST':
        
        # if text is selected        
        if 'text' in request.POST:
            context['qr_object'] = qr_creator(request.POST, request.user, 'text')
            return render(request, template, context)

        # if Url is selected
        elif 'url' in request.POST:
            context['qr_object'] = qr_creator(request, request.user, 'url')
            return render(request, template, context)

        # if github  is selected
        elif 'github' in request.POST:
            context['qr_object'] = qr_creator(request, request.user, 'github')
            return render(request, template, context)

        # if zoom  is selected
        elif 'zoom' in request.POST:
            context['qr_object'] = qr_creator(request, request.user, 'zoom')
            return render(request, template, context)

        # if App-store is selected
        elif 'app-store' in request.POST:
            context['qr_object'] = qr_creator(request, request.user, 'app-store')
            return render(request, template, context)

    return render(request, template, context)

def folders(request):
    template = 'qr_generator/dashboard/folders.html'
    context = {}

    # Get all the saved QR ID's
    user_items = [item.qr_code for item in UserCollection.objects.filter(qr_user=request.user)]

    # fetch them
    all_user_items = QRCollection.objects.filter(id__in=user_items)

    unique_categories = {str(_.category) for _ in all_user_items }
    context['folders'] = unique_categories

    return render(request, template, context)

def save_qr(request, id):
    user = request.user
    UserCollection.objects.create(qr_user=user, qr_code=id)
    messages.success(request, 'Your QR has been saved!! Go to Your Dashboard to view it')
    return  render(request, 'qr_generator/generateqr.html')

def form(request, template):
    form = ContactUsForm()
    return render(request, "qr_generator/" + template +'.html', {"form":form})

def about_us(request):
    return render(request, 'base/about_us.html', )


def contact_us(request):
    template = 'base/contact_us.html'
 
    context = {}
    if request.method == "POST":
        form =  ContactUsForm(request.POST)
        if form.is_valid():
            from_email = settings.QR_EMAIL_HOST_USER
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message'] #request.POST.get('message')
            reciever = settings.QR_EMAIL_HOST_USER

            try:
                send_mail(subject, message, from_email, [reciever,])
                messages.success(request, message="Message Successfully sent!!")
                return redirect('qr_generator:home')
            except BadHeaderError:
                messages.error(request, message="Invalid Header")
                return HttpResponse('Invalid header found.')

            except SMTPServerDisconnected:
                messages.error(request, message="Network Connection failed")
                return redirect(to='qr_generator:contact_us')

            except Exception as err:
                return HttpResponse("We haven't encountered this problem before") # TODO: will fix this when error page comes

        else:
            messages.info(request, 'One or more fields are empty!!')
            return render(request, template, context)

            
    else:
        form = ContactUsForm()

    context['form'] = form
    
    return render(request, template, context)


# Define function to download pdf file using template
def download_file(request, id='', file_type=''):


    if id != '':
        file = QRCollection.objects.get(id=id).qr_code
        obj = MEDIA_ROOT + '/' + str(file)


        match file_type:
            case 'pdf':
                filepath, filename = convert_to_pdf(obj)
            
            case 'png':
                filepath, filename = convert_to_png(obj)

            case 'jpg':
                filepath, filename = convert_to_jpg(obj)

            case 'svg':
                filepath, filename = convert_to_svg(obj)
            
            case 'jpeg':
                filepath, filename = convert_to_jpeg(obj)

        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

def learn_more(request):
    return render(request, 'base/coming_soon.html')

def page_not_found(request, exception):
    return render(request, 'base/error404.html', status=404)

