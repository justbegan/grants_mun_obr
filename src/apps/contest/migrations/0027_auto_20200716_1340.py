# Generated by Django 3.0.6 on 2020-07-16 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0026_auto_20200531_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoresheet',
            name='additional_score2',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, verbose_name='Если Заявитель является организацией, оказывающей информационную, консультационную, методическую, образовательную, экспертную и иную поддержку социально ориентированным некоммерческим организациям, возглавляющим рейтинг эффективности деятельности за предыдущий отчетный период, разработанного Уполномоченным органом, размещаемом на Портале'),
        ),
    ]