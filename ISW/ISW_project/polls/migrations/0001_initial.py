# Generated by Django 4.2.5 on 2023-10-21 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrello',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('completato', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField(max_length=250)),
                ('descrizione', models.TextField(max_length=400)),
                ('prezzo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.TextField(max_length=250)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_carta', models.TextField()),
                ('numero_carta', models.IntegerField()),
                ('scadenza', models.DateField()),
                ('cvv', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ordine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField(max_length=150)),
                ('cognome', models.TextField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('indirizzo', models.TextField(max_length=254)),
                ('stato', models.TextField(max_length=254)),
                ('citta', models.TextField(max_length=150)),
                ('regione', models.TextField(max_length=150)),
                ('provincia', models.TextField(max_length=150)),
                ('codice_postale', models.TextField(max_length=10)),
                ('pagamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.pagamento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='ElementoOrdine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField(max_length=250)),
                ('descrizione', models.TextField(max_length=400)),
                ('prezzo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.TextField(max_length=250)),
                ('ordine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.ordine')),
            ],
            options={
                'verbose_name': 'Sold Product',
                'verbose_name_plural': 'Sold Products',
            },
        ),
        migrations.CreateModel(
            name='ElementoCarrello',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantita', models.IntegerField(default=0)),
                ('carrello', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elementiCarrello', to='polls.carrello')),
                ('prodotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elementi', to='polls.prodotto')),
            ],
            options={
                'verbose_name': 'CartProduct',
                'verbose_name_plural': 'CartProducts',
            },
        ),
    ]
