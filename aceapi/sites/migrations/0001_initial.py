# Generated by Django 3.0.5 on 2020-11-26 05:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canonical', models.TextField(blank=True, default='')),
                ('robots_meta', models.TextField(blank=True, default='')),
                ('meta_description', models.TextField(blank=True, default='')),
                ('dynamic', models.BooleanField(default=False)),
                ('route', models.TextField(blank=True, default='/')),
                ('name', models.TextField()),
                ('extension', models.TextField(blank=True, default='.html')),
                ('title', models.TextField(blank=True, default='')),
                ('h_one', models.TextField(blank=True, default='')),
                ('h_two', models.TextField(blank=True, default='')),
                ('mime_type', models.TextField(blank=True, default='text/html')),
                ('display_name', models.TextField(blank=True, default='')),
                ('content', models.TextField(blank=True, default='')),
                ('draft', models.TextField(blank=True, default='')),
                ('backup', models.TextField(blank=True, default='')),
                ('metas', models.TextField(blank=True, default='')),
                ('links', models.TextField(blank=True, default='')),
                ('stylesheet', models.TextField(blank=True, default='')),
                ('header', models.TextField(blank=True, default='')),
                ('footer', models.TextField(blank=True, default='')),
                ('scripts', models.TextField(blank=True, default='')),
                ('custom_script', models.TextField(blank=True, default='')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='profiles.Profile')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('name', models.TextField(blank=True, default='')),
                ('title', models.TextField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('represents', models.TextField(blank=True, default='company')),
                ('company_name', models.TextField(blank=True, default='')),
                ('logo', models.ImageField(blank=True, upload_to='logos', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('logo_url', models.TextField(blank=True, default='')),
                ('logo_width', models.TextField(blank=True, default='')),
                ('logo_height', models.TextField(blank=True, default='')),
                ('logo_caption', models.TextField(blank=True, default='')),
                ('search_url', models.TextField(blank=True, default='')),
                ('twitter_username', models.TextField(blank=True, default='')),
                ('twitter_card', models.TextField(blank=True, default='summary_large_image')),
                ('facebook_url', models.TextField(blank=True, default='')),
                ('linkedin_url', models.TextField(blank=True, default='')),
                ('language', models.TextField(blank=True, default='en-US')),
                ('char_set', models.TextField(blank=True, default='UTF-8')),
                ('metas', models.TextField(blank=True, default='')),
                ('links', models.TextField(blank=True, default='')),
                ('stylesheet', models.TextField(blank=True, default='')),
                ('header', models.TextField(blank=True, default='')),
                ('auto_menu', models.BooleanField(default=False)),
                ('menu', models.TextField(blank=True, default='')),
                ('footer', models.TextField(blank=True, default='')),
                ('scripts', models.TextField(blank=True, default='')),
                ('custom_script', models.TextField(blank=True, default='')),
                ('sitemap_link_count', models.IntegerField(blank=True, default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sites', to='profiles.Profile')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Shortcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mime_type', models.TextField(blank=True, default='text/plain')),
                ('key', models.TextField()),
                ('value', models.TextField(blank=True, default='')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shortcodes', to='sites.Page')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shortcodes', to='sites.Site')),
            ],
            options={
                'ordering': ('-key',),
            },
        ),
        migrations.AddField(
            model_name='page',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='sites.Site'),
        ),
    ]
