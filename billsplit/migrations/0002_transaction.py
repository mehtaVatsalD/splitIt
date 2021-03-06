# Generated by Django 2.1.3 on 2018-11-13 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billsplit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('time', models.DateTimeField(verbose_name='Transaction Time')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billsplit.Group')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
