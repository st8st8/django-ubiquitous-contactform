# Generated by Django 3.2.15 on 2023-01-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubiquitous_contactform', '0002_enquiry_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='user_agent',
            field=models.TextField(blank=True, null=True),
        ),
    ]