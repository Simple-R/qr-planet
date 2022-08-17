# account/views.py
import base64
from pathlib import Path
from pickletools import read_unicodestring1
from smtplib import SMTPServerDisconnected
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings

from django.core.mail import send_mail
from django.contrib import messages

from .forms import ContactUsForm 
import qrcode
from PIL import Image
from django.conf import settings
from qr_gen_project.settings import  MEDIA_ROOT
import datetime
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
import qrcode

import qrcode.image.svg

User = get_user_model()

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


@login_required(login_url="/qr-gen/accounts/login")
def generate_qr(request):
    context = {}
    template = 'qr_generator/generateqr.html'
    
    if request.method == 'POST':

        # if text is selected        
        if 'text' in request.POST:
            QRCollection.objects.create(
                qr_user = request.user,
                category = 'TEXT',
                qr_info = 'Your Text is: ' + request.POST['text'],
                )

            ls = QRCollection.objects.all().order_by('-id')[0]
            context = {'qr_image':ls}

            return render(request, 'qr_generator/common/url_qr.html', context)

        # if Url is selected
        elif 'url-link' in request.POST:
            QRCollection.objects.create(
                qr_user = request.user,
                category = 'URL',
                qr_info = 'Your Link is: ' + request.POST['url-link'],
                )

            ls = QRCollection.objects.all().order_by('-id')[0]
            context = {'qr_image':ls}

            return render(request, 'qr_generator/common/url_qr.html', context)


        # if App-store is selected
        elif 'app-store' in request.POST:
            QRCollection.objects.create(
                qr_user = request.user,
                category = 'URL',
                qr_info = 'Your App-store Link is: ' + request.POST['app'],
                )

            ls = QRCollection.objects.all().order_by('-id')[0]
            context = {'qr_image':ls}

            return render(request, 'qr_generator/common/url_qr.html', context)
    
    return render(request, template, context)


def category(request, pk):
    if pk == "image":
        return 'image'

def save_qr(request, id):
    user = request.user
    UserCollection.objects.create(qr_user=user, qr_code=id)
    print('saved')
    messages.success(request, 'Your QR has been saved!! Go to You Dashboard to view it')
    return  render(request, 'qr_generator/generateqr.html')

def form(request, template):
    form = ContactUsForm()
    return render(request, "qr_generator/" + template +'.html', {"form":form})


def contact_us(request):
 
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
                return redirect(to='qr_generator:contact')

            except Exception as err:
                return HttpResponse("We haven't encountered this problem before") # TODO: will fix this when error page comes

            
    else:
        form = ContactUsForm()

    context['form'] = form
    
    return render(request, 'qr_generator/contact.html', context)




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

