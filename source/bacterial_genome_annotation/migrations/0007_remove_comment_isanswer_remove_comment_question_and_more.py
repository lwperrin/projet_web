# Generated by Django 4.1.4 on 2023-01-31 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacterial_genome_annotation', '0006_remove_blasthit_ident_remove_blasthit_lenn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='isAnswer',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='question',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='0', max_length=32, unique=True, verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=32, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=32, verbose_name='last name'),
        ),
    ]