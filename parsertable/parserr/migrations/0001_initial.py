# Generated by Django 4.0 on 2022-05-09 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dannie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('domain', models.TextField()),
                ('create_date', models.TextField()),
                ('update_date', models.TextField()),
                ('country', models.TextField()),
                ('isDead', models.TextField()),
                ('A', models.TextField()),
                ('NS', models.TextField()),
                ('CNAME', models.TextField()),
                ('MX', models.TextField()),
                ('TXT', models.TextField()),
            ],
        ),
    ]