from django.db import models
from BunnyCDN.Storage import Storage
from BunnyCDN.CDN import CDN
from app.BunnyStorage import BunnyStorage
from django.utils import timezone
from app.Bunny import TusFileUploader
from django.db import transaction
from app.TestSeries import TestSeriesExtractor
from app.Cloudfare import CloudfareSdk
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import unicodedata
import binascii
import os


class User(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100,blank=True,null=True)
    password = models.CharField(max_length=400)
    phone = models.CharField(unique=True, max_length=10)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.PositiveBigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    image = models.ImageField(storage=BunnyStorage(), blank=True, null=True)
    is_institute = models.BooleanField(default=False)

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )
    
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

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
        return self.username
    

    class Meta:
        managed = True
        db_table = 'user'



class AuthToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField(default=timezone.now())
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
    


    class Meta:
        managed = True
        db_table = 'auth_token'


class Otp(models.Model):
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(unique=True, max_length=10)
    otp = models.CharField(max_length=6)
    created = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'otp'

    def __str__(self):
        return self.otp


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


class Playlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now())
    date_updated = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'playlist'

    def __str__(self):
        return self.name


class Institute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    banner = models.ForeignKey(Banner,on_delete=models.CASCADE)
    director_name = models.CharField(max_length=150)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, related_name='institute_users',verbose_name="Followers")
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
        return f"{self.user.username} of {self.name}"

    class Meta:
        managed = True
        db_table = 'institute'


class InstituteUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    institute_id = models.BigIntegerField()
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'institute_users'


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, related_name='course_users',verbose_name="Enrolled Users")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    banners = models.ManyToManyField(Banner, blank=True)
    collection = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    demo_video = models.FileField(storage=TusFileUploader(instance=None), blank=True, null=True)
    pdf = models.FileField(storage=BunnyStorage(), blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    image = models.ImageField(storage=BunnyStorage(), null=True, blank=True)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    faqs = models.JSONField(default={})

    def createFileImage(self):
        """
        Generate the BunnyCDN directory path for the image dynamically.
        """
        return f"course/{self.id}/"
    
    def createDocDir(self):
        """Generate the BunnyCDN directory path for the image dynamically."""
        if self.pk:
            return f"course/{self.id}/pdf/"
        return "course/general/pdf/"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the BunnyStorage dynamically.
        """
        if self.pk:
            previous = Course.objects.filter(pk=self.pk).values("image").first()
            if previous and previous["image"] != self.image.name:
                directory = self.createFileImage()
                self.image.storage = BunnyStorage(directory)
                
            if self.collection is None:
                name = f"{self.institute.name}-{self.name}"
                collection = TusFileUploader(instance=None)
                status,value =  collection.createCollection(name)
                if not status:
                    raise Exception(f"Failed to create collection: {str(value)}")
                self.collection = value

        if self._state.adding:
            name = f"{self.institute.name}-{self.name}"
            collection = TusFileUploader(instance=None)
            status,value =  collection.createCollection(name)
            if not status:
                raise Exception(f"Failed to create collection: {str(value)}")
            self.collection = value
            directory = self.createFileImage()
            self.image.storage = BunnyStorage(directory)

        if self.demo_video:
            self.demo_video.storage = TusFileUploader(instance=self)
        if self.pdf:
            self.pdf.storage = BunnyStorage(self.createDocDir())
                
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'course'


class CourseVideos(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(storage=TusFileUploader(instance=None), blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    views  = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())


    def save(self, *args, **kwargs):
        """
        Override the save method to set the BunnyStorage dynamically.
        """
        if self.video:
            self.video.storage = TusFileUploader(instance=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'course_videos'
        

class VideoComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    video = models.ForeignKey(CourseVideos, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.user.username} commented on {self.video.name}"
    
    class Meta:
        managed = True
        db_table = 'video_comment'


class VideoLike(models.Model):
    id = models.BigAutoField(primary_key=True)
    video = models.ForeignKey(CourseVideos, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return f"{self.user.username} liked {self.video.name}"

    class Meta:
        managed = True
        db_table = 'video_like'


class CourseLiveStream(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    live = models.CharField(max_length=300, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    scheduled = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'course_live_stream'

    def save(self, *args, **kwargs):
        course_words = self.course.name.strip().split()[:10]  # take first 10 words
        course_name_trimmed = ' '.join(course_words)
        name = f"{self.name}-({course_name_trimmed})"
        cloudfare = CloudfareSdk()
        metadata = cloudfare.createLiveInput(name)

        if(metadata.get("success") == True):
            self.metadata = metadata
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        



class TestSeries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(storage=BunnyStorage(), blank=True, null=True)
    course = models.ForeignKey(to=Course,blank=True, null=True,on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    questions = models.JSONField(blank=True,null=True)
    timer = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())


    class Meta:
        managed = True
        db_table = 'test_series'

    def __str__(self):
        return self.name
    
    
    def createDocDir(self):
        """Generate the BunnyCDN directory path for the image dynamically."""
        if self.course:
            return f"course/{self.course.id}/docs/"
        return "course/general/docs/"
       

    def save(self, *args, **kwargs):
        """Override save method to process questions from .docx."""
        # Assign name if not set
        if not self.name:
            self.name = self.file.name
            
        is_new = self.pk is None  # Check if instance is being created

        if is_new and self.file:
            self.file.storage = BunnyStorage(self.createDocDir())  # Set correct storage path

        if self.questions:
            super().save(*args,**kwargs)
        
        if self.file and is_new and not self.questions:
            latest_id = TestSeries.objects.order_by('-id').first()
            next_id = latest_id.id + 1 if latest_id else 1
            
            extractor = TestSeriesExtractor(file= self.file,name=self.file.name,id=next_id)
            questions, solutions = extractor.extract_questions()
            self.questions = questions

            with transaction.atomic():
                super().save(*args, **kwargs)  # Save `TestSeries` first
                if solutions and is_new:
                    TestSeriesSolution.objects.create(test_series=self, solution=solutions)


        if not is_new:
            super().save(*args, **kwargs)


    
class TestSeriesAttempt(models.Model):
    id = models.BigAutoField(primary_key=True)
    test_series = models.ForeignKey(to=TestSeries,on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    result = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    submitted = models.BooleanField(default=False)
    total_score = models.FloatField()
    total_marks = models.FloatField()
    percentile = models.FloatField(blank=True, null=True)
    rank = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'test_series_attempt'

    def __str__(self):
        return self.user.username


class TestSeriesSolution(models.Model):
    id = models.BigAutoField(primary_key=True)
    test_series = models.ForeignKey(to=TestSeries,on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    solution = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'test_series_solution'

    def __str__(self):
        return self.test_series.name
    

class Documents(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(to=Course,blank=True, null=True,on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(storage=BunnyStorage(), blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = False
        db_table = 'documents'

    def __str__(self):
        return self.name
    
    def createDocDir(self):
        """Generate the BunnyCDN directory path for the image dynamically."""
        if self.course:
            return f"course/{self.course.id}/docs/"
        return "course/general/docs/"
    
    def save(self, *args, **kwargs):
        """Override save method to process questions from .docx."""
        # Assign name if not set
        if not self.name:
            self.name = self.file.name
            
        is_new = self.pk is None
        if is_new and self.file:
            self.file.storage = BunnyStorage(self.createDocDir())
            super().save(*args, **kwargs)

        if not is_new:
            super().save(*args, **kwargs)


communityChoice = (
    ('image', 'Image'),
    ('link', 'Link'),
    ('poll', 'Poll'),
    ("quiz", "Quiz"),
)

class CommunityPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    options = models.JSONField(blank=True, null=True)
    image = models.FileField(storage=BunnyStorage(), blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=300,choices=communityChoice)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'community_post'

    def __str__(self):
        return self.name[:50]
    
    def createDocDir(self):
        """Generate the BunnyCDN directory path for the image dynamically."""
        if self.institute:
            return f"institute/{self.institute.id}/posts/"
        return "institute/general/posts/"
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image.storage = BunnyStorage(self.createDocDir())

        super().save(*args, **kwargs)


class CommunityComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'community_comment'
        unique_together = ('post', 'user', 'comment')


class CommunityLike(models.Model):
    id = models.BigAutoField(primary_key=True)
    post= models.ForeignKey(CommunityPost, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'community_like'
        unique_together = ('post', 'user')


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_data = models.TextField()  # This field type is a guess.
    status = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=400, blank=True, null=True)
    order_id = models.CharField(max_length=400, blank=True, null=True)
    signature = models.CharField(max_length=400, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'order'
        

"""class InstituteBanners(models.Model):
    id = models.BigAutoField(primary_key=True)
    institute_id = models.BigIntegerField()
    banner_id = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'institute_banners'"""




"""class TestRel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    banners = models.ManyToManyField(Banner)


    def __str__(self):
        return f'{self.user.name}'"""


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(storage=BunnyStorage(), blank=True, null=True)
    type = models.CharField(max_length=50, choices=(('Video', 'Video'), ('TestSeries', 'TestSeries'),('Pdf', 'Pdf')), default='Video')
    schedule_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'schedule'

    def createDocDir(self):
        """Generate the BunnyCDN directory path for the image dynamically."""
        if self.course:
            return f"course/{self.course.id}/schedules/"
        return "course/schedules/"
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image.storage = BunnyStorage(self.createDocDir())

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Doubt(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(storage=BunnyStorage(), blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    
    class Meta:
        managed = True
        db_table = 'doubt'

    def createDocDir(self):
        """Generate the BunnyCDN directory path for the image dynamically."""
        if self.course:
            return f"course/{self.course.id}/doubts/"
        return "course/doubts/"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file.storage = BunnyStorage(self.createDocDir())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.question[:50]}"

