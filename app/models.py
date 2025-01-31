from django.db import models
from BunnyCDN.Storage import Storage
from BunnyCDN.CDN import CDN
from app.BunnyStorage import BunnyStorage
from django.utils import timezone

def uploadToBunny(instance, filename):
    """
    Upload an in-memory file directly to BunnyCDN.
    """
    storage = BunnyStorage()
    file_content = instance.photos.file.read()
    response = storage.uploadImage(file_content, filename)
    if response[0]:
        return response[1]
    else:
        raise Exception(response[1])


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
    date_joined = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    image = models.ImageField(storage=BunnyStorage(), blank=True, null=True)
    is_institute = models.BooleanField(default=False)

    def createFileImage(self):
        """
        Generate the BunnyCDN directory path for the image dynamically.
        """
        return f"user/{self.id}/"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the BunnyStorage dynamically.
        """
        if not self._state.adding:  # Ensures that 'id' is available
            directory = self.createFileImage()
            self.image.storage = BunnyStorage(directory)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
    

    class Meta:
        managed = True
        db_table = 'user'



class AuthToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField(default=timezone.now())
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.key

    class Meta:
        managed = True
        db_table = 'auth_token'


class Banner(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image = models.ImageField(storage=BunnyStorage())
    date_created = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(default=timezone.now())

    def createFileImage(self):
        """
        Generate the BunnyCDN directory path for the image dynamically.
        """
        return f"banner/{self.id}/"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the BunnyStorage dynamically.
        """
        if not self._state.adding:  # Ensures that 'id' is available
            directory = self.createFileImage()
            self.image.storage = BunnyStorage(directory)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'banner'


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'category'

class Institute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    banners = models.ManyToManyField(Banner)
    director_name = models.CharField(max_length=150)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(default=timezone.now())
    image = models.ImageField(storage=BunnyStorage(), null=True, blank=True)

    def createFileImage(self):
        """
        Generate the BunnyCDN directory path for the image dynamically.
        """
        return f"institute/{self.id}/"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the BunnyStorage dynamically.
        """
        if not self._state.adding:  # Ensures that 'id' is available
            directory = self.createFileImage()
            self.image.storage = BunnyStorage(directory)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'institute'


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    image = models.ImageField(storage=BunnyStorage(), null=True, blank=True)

    def createFileImage(self):
        """
        Generate the BunnyCDN directory path for the image dynamically.
        """
        return f"course/{self.id}/"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the BunnyStorage dynamically.
        """
        if not self._state.adding:  # Ensures that 'id' is available
            directory = self.createFileImage()
            self.image.storage = BunnyStorage(directory)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'course'


class CourseVideo(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="videos", blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = False
        db_table = 'course_video'



"""class InstituteBanners(models.Model):
    id = models.BigAutoField(primary_key=True)
    institute_id = models.BigIntegerField()
    banner_id = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'institute_banners'"""




class TestRel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    banners = models.ManyToManyField(Banner)


    def __str__(self):
        return f'{self.user.name}'