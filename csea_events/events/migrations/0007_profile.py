# Generated by Django 2.2 on 2019-04-18 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0006_event_approval'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('cse', 'Computer Science & Engineering'), ('ece', 'Electronics & Communication Engineering'), ('me', 'Mechanical Engineering'), ('ce', 'Civil Engineering'), ('dd', 'Design'), ('bsbe', 'Biosciences & Bioengineering'), ('cl', 'Chemical Engineering'), ('cst', 'Chemical Science & Technology'), ('eee', 'Electronics & Electrical Engineering'), ('ma', 'Mathematics & Computing'), ('ph', 'Engineering Physics'), ('rt', 'Rural Technology'), ('hss', 'Humanities & Social Sciences'), ('enc', 'Centre for Energy'), ('env', 'Centre for Environment'), ('nt', 'Centre for Nanotechnology'), ('lst', 'Centre for Linguistic Science & Technology')], max_length=100)),
                ('program', models.CharField(choices=[('btech', 'BTech'), ('mtech', 'MTech'), ('phd', 'PhD'), ('msc', 'MSc'), ('msr', 'MS-R'), ('ma', 'MA'), ('bdes', 'BDes'), ('mdes', 'MDes')], max_length=100)),
                ('roll_no', models.BigIntegerField(unique=True)),
                ('phone_no', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
