# Generated by Django 4.0.2 on 2022-03-02 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('role', models.PositiveSmallIntegerField(choices=[(2, 'Professor'), (1, 'Aluno')])),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('email', models.EmailField(max_length=120, unique=True, verbose_name='email')),
                ('first_name', models.CharField(max_length=45, verbose_name='first name')),
                ('last_name', models.CharField(max_length=45, verbose_name='last name')),
                ('birth_date', models.DateField(verbose_name='birth date')),
                ('date_joined', models.DateField(auto_now=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('avatar', models.ImageField(blank=True, max_length=1024, null=True, upload_to='', verbose_name='avatar')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
