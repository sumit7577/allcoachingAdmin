# Generated by Django 4.2.3 on 2023-12-30 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='account_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='account_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='ins',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.questionreport'),
        ),
        migrations.AddField(
            model_name='institute',
            name='product_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
