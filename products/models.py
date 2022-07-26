from django.db import models
from private_storage.fields import PrivateFileField

from . import ProductType

class ProductPermission(models.Model):
    title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="عنوان",
    )
    description = models.CharField(
        max_length=512, 
        null=True,
        blank=True,
        verbose_name="توضیحات",
    )
    device_count_permission = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="دسترسی تعداد دیوایس",
    )
    
    class Meta:
        verbose_name = "دسترسی"
        verbose_name_plural = "دسترسی ها"

    def __str__(self):
        return self.title if self.title else self.id


class ProductFile(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name="عنوان فایل",
        null=True,
        blank=True,
    )
    associated_file = PrivateFileField(
        upload_to='products/', 
        verbose_name="فایل"
    )
    
    class Meta:
        verbose_name = "فایل محصول"
        verbose_name_plural = "فایل ها"

    def __str__(self):
        return self.name


class PieceOfCode(models.Model):
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="عنوان"
    )
    code = models.TextField()
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "کد"
        verbose_name_plural = "کد ها"

    def __str__(self):
        return self.name if self.name else self.id


# wordpress product replica
class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="نام محصول")
    slug = models.SlugField(
        allow_unicode=True, verbose_name="نامک",
        null=True, 
        blank=True,
    )
    permalink = models.URLField(null=True, blank=True)
    wp_product_id = models.PositiveIntegerField(unique=True, verbose_name="آی دی محصول در وردپرس")
    status = models.CharField(max_length=32, verbose_name="وضعیت")
    permissions = models.ManyToManyField(ProductPermission, verbose_name="دسترسی ها", blank=True)
    files = models.ManyToManyField(ProductFile, verbose_name="فایل(ها)", blank=True)
    codes = models.ManyToManyField(PieceOfCode, verbose_name="کد(ها)", blank=True)
    product_type = models.CharField(
        max_length=20, 
        choices=ProductType.CHOICES,
        default=ProductType.NORMAL,
        verbose_name="نوع"
    )
    plugins = models.ManyToManyField(
        "self", 
        limit_choices_to={"product_type": ProductType.PLUGIN},
        blank=True,
        verbose_name="پلاگین(ها)"
    )

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

    @property
    def device_count_limit(self):
        count = 0
        for perm in self.permissions.all():
            count += perm.device_count_permission
        return count
