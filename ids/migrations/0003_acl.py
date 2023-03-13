# Generated by Django 4.1.7 on 2023-03-11 09:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ids', '0002_remove_acltypes_acl_remove_acltypes_type_delete_acl_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ACL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='Beschreibung')),
                ('beginn', models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Beginn')),
                ('ende', models.DateField(default=datetime.date(2070, 12, 31), null=True, verbose_name='Ende')),
                ('identifikation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ids.identifikation', verbose_name='ID Karte')),
                ('type', models.ManyToManyField(to='ids.acltyp', verbose_name='Typ')),
            ],
        ),
    ]