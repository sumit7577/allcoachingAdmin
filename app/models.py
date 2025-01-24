from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=400)
    phone = models.CharField(unique=True, max_length=13)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.PositiveBigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    date_joined = models.DateTimeField()
    date_updated = models.DateTimeField()
    is_active = models.IntegerField()
    image = models.CharField(max_length=300, blank=True, null=True)
    is_institute = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'user'

        

class AuthToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user_id = models.PositiveBigIntegerField(unique=True)

    class Meta:
        managed = True
        db_table = 'auth_token'


class Banner(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'banner'


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'category'


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    institute_id = models.BigIntegerField()
    category_id = models.BigIntegerField(blank=True, null=True)
    banner_id = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'course'


class Institute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    category_id = models.BigIntegerField(blank=True, null=True)
    director_name = models.CharField(max_length=150)
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'institute'


class InstituteBanners(models.Model):
    id = models.BigAutoField(primary_key=True)
    institute_id = models.BigIntegerField()
    banner_id = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'institute_banners'




class TestRel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    banners = models.ManyToManyField(Banner)

    def __str__(self):
        return f'{self.user.name}'