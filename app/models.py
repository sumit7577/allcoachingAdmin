from django.db import models

# Create your models here.
class Admin(models.Model):
    id = models.BigIntegerField(primary_key=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.email

    class Meta:
        managed = True
        db_table = 'admin'


class AdminBlogs(models.Model):
    id = models.BigIntegerField(primary_key=True)
    add_date = models.DateTimeField(blank=True, null=True)
    blog_body = models.TextField(blank=True, null=True)
    blog_feature_image = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = 'admin_blogs'


class AdminConfig(models.Model):
    id = models.BigIntegerField(primary_key=True)
    payment_commission = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.payment_commission

    class Meta:
        managed = True
        db_table = 'admin_config'


class AdminTestSeriesCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'admin_test_series_category'


class AdminTestSeriesSubCategoryContent(models.Model):
    id = models.BigIntegerField(primary_key=True)
    add_date = models.DateTimeField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()
    test_series_sub_category_id = models.BigIntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'admin_test_series_sub_category_content'


class AdminTestSubCategories(models.Model):
    id = models.BigIntegerField(primary_key=True)
    add_date = models.DateTimeField(blank=True, null=True)
    category_id = models.BigIntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'admin_test_sub_categories'


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()
    span = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'category'


class ContactUs(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'contact_us'


class Course(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fees = models.FloatField()
    inst_id = models.BigIntegerField()
    is_deleted = models.TextField()  # This field type is a guess.
    leads = models.BigIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = 'course'


class CourseBanners(models.Model):
    id = models.BigIntegerField(primary_key=True)
    add_date = models.DateTimeField(blank=True, null=True)
    banner_image_link = models.CharField(max_length=255, blank=True, null=True)
    banner_link = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.BigIntegerField()
    place_holder = models.CharField(max_length=255, blank=True, null=True)
    published = models.TextField()  # This field type is a guess.

    def __str__(self) -> str:
        return self.place_holder

    class Meta:
        managed = True
        db_table = 'course_banners'


class CourseDocument(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    date = models.DateTimeField(blank=True, null=True)
    file_address = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.TextField()  # This field type is a guess.
    is_demo = models.TextField()  # This field type is a guess.
    name = models.CharField(max_length=255, blank=True, null=True)
    playlist_id = models.BigIntegerField()
    published = models.TextField()  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'course_document'


class CourseGoLive(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    date = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    video_url_json = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = 'course_go_live'


class CourseTimeTableItem(models.Model):
    id = models.BigIntegerField(primary_key=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    ins_id = models.BigIntegerField()
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    subject_id = models.BigIntegerField()
    time = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = 'course_time_table_item'


class CourseTimeTableSubject(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'course_time_table_subject'


class CourseVideo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.BigIntegerField()
    date = models.DateTimeField(blank=True, null=True)
    demo_lenght = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.TextField()  # This field type is a guess.
    is_demo = models.TextField()  # This field type is a guess.
    is_streaming = models.TextField()  # This field type is a guess.
    live_class_date = models.CharField(max_length=255, blank=True, null=True)
    live_class_time = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    playlist_id = models.BigIntegerField()
    published = models.TextField()  # This field type is a guess.
    time_stamp = models.DateTimeField(blank=True, null=True)
    video_format_json = models.TextField(blank=True, null=True)
    video_location = models.TextField(blank=True, null=True)
    video_thumb = models.CharField(max_length=255, blank=True, null=True)
    video_type = models.CharField(max_length=255, blank=True, null=True)
    views = models.BigIntegerField()
    bunny_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'course_video'


class CourseVideoComments(models.Model):
    id = models.BigIntegerField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    comment_time = models.DateTimeField(blank=True, null=True)
    video_id = models.BigIntegerField()
    student = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.comment

    class Meta:
        managed = True
        db_table = 'course_video_comments'


class DocumentPlaylist(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'document_playlist'


class Feed(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category_id = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    creation_time = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    edited = models.TextField()  # This field type is a guess.
    feed_liker_ins = models.CharField(max_length=255, blank=True, null=True)
    feed_liker_student = models.CharField(max_length=255, blank=True, null=True)
    feed_type = models.IntegerField()
    ins_id = models.BigIntegerField()
    likes = models.IntegerField()
    photo_location = models.CharField(max_length=255, blank=True, null=True)
    poll_question = models.TextField(blank=True, null=True)
    poll_voted_institutes = models.CharField(max_length=255, blank=True, null=True)
    poll_voted_students = models.CharField(max_length=255, blank=True, null=True)
    posted_by = models.IntegerField()
    student_id = models.BigIntegerField()
    tags = models.CharField(max_length=255, blank=True, null=True)
    total_poll_votes = models.IntegerField()
    voter_type = models.IntegerField()

    def __str__(self):
        return self.tags

    class Meta:
        managed = True
        db_table = 'feed'


class FeedCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'feed_category'


class FeedComments(models.Model):
    id = models.BigIntegerField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    commenter = models.IntegerField()
    feed_id = models.BigIntegerField()
    ins_id = models.BigIntegerField()
    student_id = models.BigIntegerField()
    time_stamp = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.comment

    class Meta:
        managed = True
        db_table = 'feed_comments'


class FeedImages(models.Model):
    id = models.BigIntegerField(primary_key=True)
    feed_id = models.BigIntegerField()
    feed_image = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self) -> str:
        return self.feed_image

    class Meta:
        managed = True
        db_table = 'feed_images'


class FeedPollOptions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    feed_id = models.BigIntegerField()
    poll_option = models.CharField(max_length=255, blank=True, null=True)
    up_votes = models.IntegerField()

    def __str__(self) -> str:
        return self.poll_option

    class Meta:
        managed = True
        db_table = 'feed_poll_options'


class FeedReport(models.Model):
    id = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_seen_by_admin = models.TextField()  # This field type is a guess.
    report_date = models.DateTimeField(blank=True, null=True)
    report_update_date = models.DateTimeField(blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    feed = models.ForeignKey(Feed, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.description

    class Meta:
        managed = True
        db_table = 'feed_report'


class HibernateSequence(models.Model):
    next_val = models.BigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.next_val

    class Meta:
        managed = True
        db_table = 'hibernate_sequence'


class InsLeads(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    ins_id = models.BigIntegerField()
    time = models.DateTimeField(blank=True, null=True)
    user_id = models.BigIntegerField()

    def __str__(self) -> str:
        return self.id

    class Meta:
        managed = True
        db_table = 'ins_leads'


class InsReview(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    ins_id = models.BigIntegerField()
    rating = models.IntegerField()
    reply = models.CharField(max_length=255, blank=True, null=True)
    review = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.BigIntegerField()
    time = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.review

    class Meta:
        managed = True
        db_table = 'ins_review'


class InsSubscription(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ins_id = models.BigIntegerField()
    is_notification_on = models.TextField()  # This field type is a guess.
    student_id = models.BigIntegerField()
    
    def __str__(self) -> str:
        return self.is_notification_on

    class Meta:
        managed = True
        db_table = 'ins_subscription'


class InsTestSeries(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category = models.BigIntegerField()
    correct_marks = models.FloatField()
    course_id = models.BigIntegerField()
    date = models.DateTimeField(blank=True, null=True)
    hidden = models.TextField()  # This field type is a guess.
    is_admin = models.TextField()  # This field type is a guess.
    is_demo = models.TextField()  # This field type is a guess.
    is_practice = models.TextField()  # This field type is a guess.
    max_marks = models.IntegerField()
    playlist_id = models.BigIntegerField()
    published = models.TextField()  # This field type is a guess.
    question_count = models.IntegerField()
    time = models.TimeField(blank=True, null=True)
    time_duration = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    wrong_marks = models.FloatField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = 'ins_test_series'


class InsTestSeriesPlaylist(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'ins_test_series_playlist'


class InsTestSeriesQuestions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    correct_opt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    optiona = models.CharField(max_length=255, blank=True, null=True)
    optionb = models.CharField(max_length=255, blank=True, null=True)
    optionc = models.CharField(max_length=255, blank=True, null=True)
    optiond = models.CharField(max_length=255, blank=True, null=True)
    option_type = models.IntegerField()
    question = models.TextField(blank=True, null=True)
    question_type = models.IntegerField()
    test_series_id = models.BigIntegerField()

    def __str__(self) -> str:
        return self.question

    class Meta:
        managed = True
        db_table = 'ins_test_series_questions'


class InsTestSeriesUserQuestionResponses(models.Model):
    id = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    user_response = models.CharField(max_length=255, blank=True, null=True)
    question = models.ForeignKey(InsTestSeriesQuestions, models.DO_NOTHING, blank=True, null=True)
    brief_fk = models.ForeignKey('InsTestSeriesUserResponseBrief', models.DO_NOTHING, db_column='brief_fk', blank=True, null=True)

    def __str__(self) -> str:
        return self.question

    class Meta:
        managed = True
        db_table = 'ins_test_series_user_question_responses'


class InsTestSeriesUserResponseBrief(models.Model):
    id = models.BigIntegerField(primary_key=True)
    accuracy = models.CharField(max_length=255, blank=True, null=True)
    correct_ques = models.IntegerField()
    percentile = models.CharField(max_length=255, blank=True, null=True)
    ranks = models.BigIntegerField()
    score = models.BigIntegerField()
    skipped_ques = models.IntegerField()
    status = models.IntegerField()
    student_id = models.BigIntegerField()
    test_series_id = models.BigIntegerField()
    time_left = models.CharField(max_length=255, blank=True, null=True)
    time_taken = models.CharField(max_length=255, blank=True, null=True)
    wrong_ques = models.IntegerField()
    rank = models.BigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.rank

    class Meta:
        managed = True
        db_table = 'ins_test_series_user_response_brief'


class Institute(models.Model):
    id = models.BigIntegerField(primary_key=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    boost_value = models.IntegerField()
    category = models.BigIntegerField()
    city = models.CharField(max_length=255, blank=True, null=True)
    director_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    expo_token = models.CharField(max_length=255, blank=True, null=True)
    five_star_count = models.IntegerField()
    followers_count = models.BigIntegerField()
    four_star_count = models.IntegerField()
    ifsc = models.CharField(max_length=255, blank=True, null=True)
    ins_streaming_secret_key = models.CharField(max_length=255, blank=True, null=True)
    leads = models.BigIntegerField()
    logo = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    one_star_count = models.IntegerField()
    password = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    three_star_count = models.IntegerField()
    total_rating = models.IntegerField()
    total_rating_count = models.IntegerField()
    total_revenue = models.BigIntegerField()
    two_star_count = models.IntegerField()
    unique_user_id = models.CharField(max_length=255, blank=True, null=True)
    upi = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'institute'


class MainBanners(models.Model):
    id = models.BigIntegerField(primary_key=True)
    banner_image_link = models.CharField(max_length=255, blank=True, null=True)
    banner_link = models.CharField(max_length=255, blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    place_holder = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.place_holder

    class Meta:
        managed = True
        db_table = 'main_banners'


class Notification(models.Model):
    id = models.BigIntegerField(primary_key=True)
    is_seen = models.TextField()  # This field type is a guess.
    message = models.CharField(max_length=255, blank=True, null=True)
    notification_for = models.IntegerField()
    notification_from = models.CharField(max_length=255, blank=True, null=True)
    notification_image = models.CharField(max_length=255, blank=True, null=True)
    notification_time = models.DateTimeField(blank=True, null=True)
    receiver_id = models.BigIntegerField()
    redirect_link = models.CharField(max_length=255, blank=True, null=True)
    sender_id = models.BigIntegerField()
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.message

    class Meta:
        managed = True
        db_table = 'notification'


class Otp(models.Model):
    id = models.BigIntegerField(primary_key=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    mobile_number_hash = models.CharField(max_length=255, blank=True, null=True)
    otp_hash = models.CharField(max_length=255, blank=True, null=True)
    otp_value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.mobile_number

    class Meta:
        managed = True
        db_table = 'otp'


class Payouts(models.Model):
    id = models.BigIntegerField(primary_key=True)
    amount = models.FloatField()
    order_id = models.CharField(max_length=255, blank=True, null=True)
    payout_time = models.DateTimeField(blank=True, null=True)
    ins = models.ForeignKey(Institute, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.ins.name

    class Meta:
        managed = True
        db_table = 'payouts'


class QuestionReport(models.Model):
    id = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    report_date = models.DateTimeField(blank=True, null=True)
    report_update_date = models.DateTimeField(blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    question = models.ForeignKey(InsTestSeriesQuestions, models.DO_NOTHING, blank=True, null=True)
    test_series = models.ForeignKey(InsTestSeries, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.question

    class Meta:
        managed = True
        db_table = 'question_report'


class Student(models.Model):
    id = models.BigIntegerField(primary_key=True)
    blocked = models.TextField()  # This field type is a guess.
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    expo_token = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    state_of_residence = models.CharField(max_length=255, blank=True, null=True)
    student_image = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'student'


class StudentHistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    item_id = models.BigIntegerField()
    student_id = models.BigIntegerField()
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.type

    class Meta:
        managed = True
        db_table = 'student_history'
        unique_together = (('type', 'item_id', 'student_id'),)


class StudentMessage(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    for_admin = models.TextField()  # This field type is a guess.
    is_seen_by_admin = models.TextField()  # This field type is a guess.
    is_seen_by_ins = models.TextField()  # This field type is a guess.
    message = models.TextField(blank=True, null=True)
    message_initial_time = models.DateTimeField(blank=True, null=True)
    message_type = models.CharField(max_length=255, blank=True, null=True)
    message_update_time = models.DateTimeField(blank=True, null=True)
    replied = models.TextField()  # This field type is a guess.
    reply = models.TextField(blank=True, null=True)
    institute = models.ForeignKey(Institute, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.message

    class Meta:
        managed = True
        db_table = 'student_message'


class StudentMessageImages(models.Model):
    id = models.BigIntegerField(primary_key=True)
    image_link = models.CharField(max_length=255, blank=True, null=True)
    is_reply_image = models.TextField()  # This field type is a guess.
    student_msg_fk = models.ForeignKey(StudentMessage, models.DO_NOTHING, db_column='student_msg_fk', blank=True, null=True)

    def __str__(self) -> str:
        return self.image_link

    class Meta:
        managed = True
        db_table = 'student_message_images'


class StudentPinList(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ins = models.ForeignKey(Institute, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        managed = True
        db_table = 'student_pin_list'


class TestSeriesQuestionResponse(models.Model):
    id = models.BigIntegerField(primary_key=True)
    is_correct = models.TextField()  # This field type is a guess.
    student_id = models.BigIntegerField()
    test_series_id = models.BigIntegerField()
    test_series_question_id = models.BigIntegerField()

    def __str__(self) -> str:
        return self.id

    class Meta:
        managed = True
        db_table = 'test_series_question_response'


class TestSeriesResponse(models.Model):
    id = models.BigIntegerField(primary_key=True)
    obtained_marks = models.IntegerField()
    student_id = models.BigIntegerField()
    test_series_id = models.BigIntegerField()
    time_stamp = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.obtained_marks

    class Meta:
        managed = True
        db_table = 'test_series_response'


class Transaction(models.Model):
    id = models.BigIntegerField(primary_key=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.BigIntegerField()
    gateway_response_msg = models.CharField(max_length=255, blank=True, null=True)
    gateway_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    ins_id = models.BigIntegerField()
    is_seen_by_admin = models.TextField()  # This field type is a guess.
    is_seen_by_ins = models.TextField()  # This field type is a guess.
    order_id = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.BigIntegerField()

    def __str__(self) -> str:
        return self.amount

    class Meta:
        managed = True
        db_table = 'transaction'


class VideoPlaylist(models.Model):
    id = models.BigIntegerField(primary_key=True)
    course_id = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'video_playlist'