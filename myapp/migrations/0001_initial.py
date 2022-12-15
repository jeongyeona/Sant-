# Generated by Django 4.1.2 on 2022-12-15 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Wine",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name_kr", models.CharField(blank=True, max_length=100, null=True)),
                ("name_en", models.CharField(blank=True, max_length=200, null=True)),
                ("producer", models.CharField(blank=True, max_length=100, null=True)),
                ("nation", models.CharField(blank=True, max_length=200, null=True)),
                ("varieties", models.CharField(blank=True, max_length=350, null=True)),
                ("type", models.CharField(blank=True, max_length=30, null=True)),
                ("food", models.CharField(blank=True, max_length=200, null=True)),
                ("abv", models.CharField(blank=True, max_length=200, null=True)),
                ("degree", models.CharField(blank=True, max_length=200, null=True)),
                ("sweet", models.IntegerField(blank=True, null=True)),
                ("acidity", models.IntegerField(blank=True, null=True)),
                ("body", models.IntegerField(blank=True, null=True)),
                ("tannin", models.IntegerField(blank=True, null=True)),
                ("price", models.IntegerField(blank=True, null=True)),
                ("year", models.CharField(blank=True, max_length=30, null=True)),
                ("ml", models.CharField(blank=True, max_length=30, null=True)),
                ("url", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={"db_table": "wine", "managed": False,},
        ),
        migrations.CreateModel(
            name="WineUser",
            fields=[
                (
                    "id",
                    models.CharField(blank=True, max_length=30, null=True, unique=True),
                ),
                ("pwd", models.CharField(blank=True, max_length=100, null=True)),
                ("nickname", models.CharField(blank=True, max_length=30, null=True)),
                ("email", models.CharField(blank=True, max_length=30, null=True)),
                ("regdate", models.DateTimeField()),
                ("pid", models.AutoField(primary_key=True, serialize=False)),
            ],
            options={"db_table": "wine_user", "managed": False,},
        ),
        migrations.CreateModel(
            name="WineGrade",
            fields=[
                (
                    "wineid",
                    models.OneToOneField(
                        db_column="wineid",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="myapp.wine",
                    ),
                ),
                ("grade", models.PositiveIntegerField()),
            ],
            options={"db_table": "wine_grade", "managed": False,},
        ),
    ]
