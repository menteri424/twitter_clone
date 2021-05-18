# Generated by Django 3.1.5 on 2021-05-18 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, unique=True, verbose_name='ユーザーID')),
                ('password', models.CharField(max_length=20, verbose_name='パスワード')),
                ('full_name', models.CharField(max_length=20, verbose_name='名前')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('profile', models.CharField(blank=True, max_length=50, null=True, verbose_name='プロフィール')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('birth_date', models.DateTimeField(blank=True, null=True, verbose_name='誕生日')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserFollowingRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee', to='user.user')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user.user')),
            ],
            options={
                'db_table': 'follower',
            },
        ),
        migrations.AddConstraint(
            model_name='userfollowingrelation',
            constraint=models.UniqueConstraint(fields=('followee', 'follower'), name='duplicated_following'),
        ),
    ]