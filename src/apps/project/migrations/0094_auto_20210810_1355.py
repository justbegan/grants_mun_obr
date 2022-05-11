# Generated by Django 3.0.14 on 2021-08-10 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0093_auto_20210625_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255, verbose_name='Мероприятие, его содержание, место проведения')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('finish_date', models.DateField(verbose_name='Дата окончания')),
                ('fulfillment', models.CharField(max_length=1000)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ReportingExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('qty', models.IntegerField(blank=True, default=None, null=True)),
                ('unit_cost', models.IntegerField(blank=True, default=None, null=True)),
                ('overall', models.IntegerField(blank=True, default=None, null=True)),
                ('planned', models.IntegerField(blank=True, default=None, null=True)),
                ('value', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportingIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('date', models.DateField(blank=True, default=None, null=True)),
                ('planned', models.IntegerField(blank=True, default=None, null=True)),
                ('value', models.IntegerField(blank=True, default=None, null=True)),
                ('reason', models.CharField(blank=True, default=None, max_length=1000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='report_accept_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата принятия отчета'),
        ),
        migrations.AddField(
            model_name='project',
            name='report_status',
            field=models.CharField(choices=[('realization', 'Реализуется'), ('expire', 'Не сдан'), ('check', 'На проверке'), ('completion', 'На доработке'), ('accept', 'Принят')], default='realization', max_length=32, verbose_name='Статус отчетности'),
        ),
        migrations.CreateModel(
            name='ReportingIndicatorLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='project.ReportingIndicator')),
            ],
        ),
        migrations.CreateModel(
            name='ReportingIndicatorFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'photo'), (1, 'doc')])),
                ('file', models.FileField(upload_to='projects/reports/2021', verbose_name='Файл')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='project.ReportingIndicator')),
            ],
        ),
        migrations.AddField(
            model_name='reportingindicator',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='project.Project'),
        ),
        migrations.CreateModel(
            name='ReportingExpenseFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='projects/reports/2021', verbose_name='Файл')),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='project.ReportingExpense')),
            ],
        ),
        migrations.AddField(
            model_name='reportingexpense',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='project.Project'),
        ),
        migrations.CreateModel(
            name='ReportingEventLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255)),
                ('reporting_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='project.ReportingEvent')),
            ],
        ),
        migrations.CreateModel(
            name='ReportingEventFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'photo'), (1, 'doc')])),
                ('file', models.FileField(upload_to='projects/reports/2021', verbose_name='Файл')),
                ('reporting_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='project.ReportingEvent')),
            ],
        ),
        migrations.AddField(
            model_name='reportingevent',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_events', to='project.Project', verbose_name='Проект'),
        ),
        migrations.CreateModel(
            name='AgreementFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('agreement', 'Соглашение'), ('additional_agreement', 'Дополнительное соглашение'), ('check_results', 'Итоги проверки')], max_length=32, verbose_name='Тип')),
                ('title', models.CharField(max_length=500, verbose_name='Наименование')),
                ('number', models.CharField(max_length=50, verbose_name='Номер')),
                ('date', models.DateField(verbose_name='Дата подписания')),
                ('file', models.FileField(upload_to='projects/agreements/2021', verbose_name='Файл')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
    ]
