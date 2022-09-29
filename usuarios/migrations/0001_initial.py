# Generated by Django 4.1.1 on 2022-09-28 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cuenta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone_number", models.CharField(max_length=50)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now_add=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superadmin", models.BooleanField(default=False)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="PerfilUsuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("direccion", models.CharField(blank=True, max_length=255)),
                (
                    "imagen_perfil",
                    models.ImageField(blank=True, upload_to="perfilusuarios"),
                ),
                ("ciudad", models.CharField(blank=True, max_length=25)),
                ("pais", models.CharField(blank=True, max_length=25)),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="usuarios.cuenta",
                    ),
                ),
            ],
        ),
    ]