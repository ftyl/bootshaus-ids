# Generated by Django 4.1.7 on 2023-03-14 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ids', '0003_acl'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acltyp',
            options={'ordering': ['name'], 'verbose_name': 'ACL Typ', 'verbose_name_plural': 'ACL Typen'},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['name'], 'verbose_name': 'Position', 'verbose_name_plural': 'Positionen'},
        ),
    ]
