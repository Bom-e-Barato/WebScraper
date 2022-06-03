# Generated by Django 4.0.5 on 2022-06-03 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('img', models.ImageField(blank=True, max_length=1024, null=True, upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('promoted', models.BooleanField(default=False)),
                ('negotiable', models.BooleanField(default=False)),
                ('category', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Others'), (1, 'Technology')], null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
