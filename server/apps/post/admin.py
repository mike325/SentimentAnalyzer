from django.contrib import admin
from .models import SocialNetwork
from .models import Location
from .models import Platform
from .models import Topic
from .models import User
from .models import Post

admin.site.register(SocialNetwork)
admin.site.register(Location)
admin.site.register(Platform)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(Post)
