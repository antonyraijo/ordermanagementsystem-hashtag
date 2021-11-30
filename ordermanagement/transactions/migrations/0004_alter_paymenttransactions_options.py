from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20211130_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymenttransactions',
            options={'verbose_name_plural': 'Payment transactions'},
        ),
    ]
