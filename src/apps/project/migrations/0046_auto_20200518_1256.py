# Generated by Django 3.0.6 on 2020-05-18 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0045_auto_20200518_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='commercial_grants',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='взносы, пожертвования российских коммерческих организаций'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='dividends',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='внереализационные доходы (дивиденды, проценты по депозитам и т.п.)'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='federal_budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='средства, полученные из федерального бюджета'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='foreign_grants',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='гранты, взносы, пожертвования иностранных организаций и иностранных граждан'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='local_budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='средства, полученные из местных бюджетов'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='membership_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='вступительные, членские и иные взносы, пожертвования российских граждан'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='other_income',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='прочие доходы'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='presidential_grants',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='президентские гранты'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='region_budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='средства, полученные из бюджетов субъектов Российской Федерации'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='доходы (выручка) от реализации товаров, работ, услуг, имущественных прав'),
        ),
    ]
