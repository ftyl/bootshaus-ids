# Generated by Django 4.1.7 on 2023-03-09 23:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import ids.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ACL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='Beschreibung')),
                ('beginn', models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Beginn')),
                ('ende', models.DateField(default=datetime.date(2070, 12, 31), null=True, verbose_name='Ende')),
            ],
        ),
        migrations.CreateModel(
            name='ACLTyp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('beschreibung', models.CharField(blank=True, max_length=256, verbose_name='Beschreibung')),
            ],
            options={
                'verbose_name': 'ACL Typ',
                'verbose_name_plural': 'ACL Typen',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('beschreibung', models.CharField(blank=True, max_length=256, verbose_name='Beschreibung')),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positionen',
            },
        ),
        migrations.CreateModel(
            name='Identifikation',
            fields=[
                ('slug', models.SlugField(default=ids.models.Identifikation.getRandomString, primary_key=True, serialize=False)),
                ('bild', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=False, null=True, quality=-1, scale=None, size=[300, 400], upload_to='photos/', verbose_name='ID-Bild')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ids.position', verbose_name='Position')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ID Karte',
                'verbose_name_plural': 'ID Karten',
            },
        ),
        migrations.CreateModel(
            name='ACLTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ids.acl')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ids.acltyp')),
            ],
        ),
        migrations.AddField(
            model_name='acl',
            name='identifikation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ids.identifikation', verbose_name='ID Karte'),
        ),
        migrations.AddField(
            model_name='acl',
            name='type',
            field=models.ManyToManyField(through='ids.ACLTypes', to='ids.acltyp', verbose_name='Typ'),
        ),
    ]
