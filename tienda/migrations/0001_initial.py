# Generated by Django 4.1.1 on 2022-10-02 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
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
                ("categoria_nombre", models.CharField(max_length=200, unique=True)),
                ("descripcion", models.TextField(max_length=500, unique=True)),
                ("slug", models.CharField(max_length=200, unique=True)),
                ("imagen", models.ImageField(upload_to="imagenes/productos")),
            ],
            options={"verbose_name": "categoria", "verbose_name_plural": "categorias",},
        ),
        migrations.CreateModel(
            name="Producto",
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
                ("producto_nombre", models.CharField(max_length=200, unique=True)),
                ("slug", models.CharField(max_length=200, unique=True)),
                ("descripcion", models.TextField(max_length=500, unique=True)),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10)),
                ("imagen", models.ImageField(upload_to="imagenes/productos")),
                ("cantidad", models.IntegerField()),
                ("disponible", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("modified_date", models.DateTimeField(auto_now=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tienda.categoria",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Variedad",
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
                (
                    "variedad_categoria",
                    models.CharField(
                        choices=[("color", "color"), ("talla", "talla")], max_length=100
                    ),
                ),
                ("variedad_valor", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tienda.producto",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductoGaleria",
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
                (
                    "imagen",
                    models.ImageField(max_length=255, upload_to="tienda/productos"),
                ),
                (
                    "producto",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tienda.producto",
                    ),
                ),
            ],
        ),
    ]
