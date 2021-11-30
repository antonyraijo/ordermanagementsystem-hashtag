from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_payable_amount',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='PaymentTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_instalment_amount', models.FloatField()),
                ('balance_amount_to_pay', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='transactions.order')),
            ],
        ),
    ]
