from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="event image 用于活动卡片和活动详情页展示，不是必填字段。",
                null=True,
                upload_to="event_images/",
            ),
        ),
    ]
