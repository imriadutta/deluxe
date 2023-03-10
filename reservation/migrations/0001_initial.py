# Generated by Django 4.1.7 on 2023-02-23 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=25)),
                ('lastname', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=20)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LoginStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.IntegerField()),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.guest')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField()),
                ('title', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
                ('passcode', models.CharField(max_length=15)),
                ('date', models.DateField(auto_now=True)),
                ('price', models.IntegerField()),
                ('features', models.CharField(max_length=500)),
                ('is_reserved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electricity', models.IntegerField()),
                ('gas', models.IntegerField()),
                ('internet', models.IntegerField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.reservation')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.room'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=25)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.reservation')),
            ],
        ),
    ]
