# Generated by Django 3.2.2 on 2021-05-17 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0003_auto_20210516_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('consumer_contact_number', models.CharField(max_length=10)),
                ('time', models.TimeField(auto_now_add=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.consumer')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.provider')),
            ],
        ),
    ]
