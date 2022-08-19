# account/models.py
from io import BytesIO
from qrcode import *
import qrcode
from django.utils import timezone
from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model
from qr_gen_project.settings import MEDIA_URL, STATIC_ROOT, STATIC_URL, MEDIA_ROOT


from django.db import models
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
OUR_LOGO = STATIC_ROOT + '/base/images/' + 'qr_logo.png'
import random
import datetime



# Todo: extend the base user model and override to __str__ method to return name
User = get_user_model()


def get_current_time():
    now = str(datetime.datetime.now()).split('.')
    return str(now[1])


class Category(models.Model):
    """Every Available category"""
    category_name = models.CharField(primary_key=True, max_length=250, unique=True)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'


class QRCollection(models.Model):
    """All QR collections available"""
    qr_user = models.ForeignKey(User, on_delete=models.CASCADE, )
    category = models.CharField(max_length=200, blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    
    qr_code = models.ImageField(upload_to='all_qr/')
    qr_info = models.CharField(max_length=200, blank=True, null=True)

    def save(self,*args,**kwargs):
        our_logo = Image.open(OUR_LOGO)
    
        # adjust image size
        widthpercent = (100/float(our_logo.size[0]))
        hsize = int((float(our_logo.size[1])*float(widthpercent)))
        our_logo = our_logo.resize((100, hsize), Image.ANTIALIAS)

        QRcode = qrcode.QRCode(
        version=3,
        box_size = 10,
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M
        )
        QRcode.add_data(self.qr_info)
        QRcode.make(fit=True)
    
        QRimg = QRcode.make_image(
            fill_color='black', back_color="white").convert('RGB')

         # set size of QR code
        pos = (
            (QRimg.size[0] - our_logo.size[0]) // 2,
            (QRimg.size[1] - our_logo.size[1]) // 2
            )

        QRimg.paste(our_logo, pos)
        buffer=BytesIO()
        QRimg.save(buffer, 'PNG')
        self.qr_code.save(f'{self.qr_user.username}{random.randint(0,9999)}.png',File(buffer),save=False)
        print(self.qr_code)
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.qr_user.username}\'s {self.category} {self.id}'


    class Meta:
        db_table = 'qr_collection'
        verbose_name_plural = 'qr_collections'

class UserCollection(models.Model):
    """A simple abstraction of the Collections for a user"""
    qr_user = models.ForeignKey(User, on_delete=models.CASCADE,)
    qr_code = models.IntegerField()

    def __str__(self):
        return str(self.qr_user)

    class Meta:
        db_table = 'user_collection'
        verbose_name_plural = 'user_collections'