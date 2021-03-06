# Generated by Django 3.1 on 2022-03-24 13:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meteorvendor', '0002_auto_20220322_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ownerproductchainaccount', models.CharField(max_length=200)),
                ('issuedyn', models.BooleanField(default='N')),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='vendor',
            new_name='vendorid',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='owneraccount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='productaccount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='productqty',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='vendoraccount',
        ),
        migrations.AddField(
            model_name='owner',
            name='insdttm',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='owner',
            name='ownerchainaccount',
            field=models.CharField(default='aa', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='owner',
            name='ownerpassword',
            field=models.CharField(default='aa', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='owner',
            name='upddttm',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='insdttm',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='upddttm',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendorchainaccount',
            field=models.CharField(default='aa', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendorid',
            field=models.CharField(default='aa', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendorpassword',
            field=models.CharField(default='aa', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='productnickname',
            field=models.CharField(default='aaa', max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OwnerProductHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changeseq', models.IntegerField(default=0)),
                ('fromownerchainaccount', models.CharField(max_length=200, null=True)),
                ('toownerchainaccount', models.CharField(max_length=200, null=True)),
                ('ownerproductchainaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteorvendor.ownerproduct')),
            ],
        ),
        migrations.AddField(
            model_name='ownerproduct',
            name='ownerid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteorvendor.owner'),
        ),
        migrations.AddField(
            model_name='ownerproduct',
            name='productid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteorvendor.product'),
        ),
    ]
