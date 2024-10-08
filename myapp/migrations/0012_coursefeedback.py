# Generated by Django 5.1.1 on 2024-09-14 16:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_course_notes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='coursefeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.CharField(blank=True, max_length=1, null=True)),
                ('review', models.CharField(blank=True, default='no feedback given', max_length=500, null=True)),
                ('course_title', models.ForeignKey(db_column='E_learning_id', on_delete=django.db.models.deletion.CASCADE, to='myapp.course')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
