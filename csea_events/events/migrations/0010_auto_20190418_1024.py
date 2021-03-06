# Generated by Django 2.2 on 2019-04-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_event_requestor'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='faq_a_1',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_a_2',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_a_3',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_a_4',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_a_5',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_android',
            field=models.CharField(blank=True, max_length=7000),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_q_1',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_q_2',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_q_3',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_q_4',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='faq_q_5',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
