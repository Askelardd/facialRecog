# Generated by Django 5.0.2 on 2024-03-04 09:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_pessoa_name_alter_pessoa_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstacaoTrabalho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('mac_address', models.CharField(max_length=17, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroAcesso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_acesso', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('estacao_trabalho', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registros_acesso', to='main.estacaotrabalho')),
                ('mac_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regis_mac_address', to='main.estacaotrabalho', to_field='mac_address')),
                ('pessoa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.pessoa')),
            ],
        ),
    ]