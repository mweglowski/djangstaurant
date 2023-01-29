# Generated by Django 4.1.5 on 2023-01-29 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='MenuItemRequirement',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ingredient')),
                ('menu_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.menuitem')),
            ],
        ),
    ]