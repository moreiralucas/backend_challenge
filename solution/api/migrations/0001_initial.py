# Generated by Django 3.2.4 on 2021-06-07 00:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gas_capacity', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('gas', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
            ],
        ),
        migrations.CreateModel(
            name='Tyre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degradation', models.PositiveSmallIntegerField(default=0)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tyre', to='api.car')),
            ],
        ),
    ]
