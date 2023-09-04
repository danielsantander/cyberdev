from django.core import serializers
from myproject.myapp import models

data = serializers.serialize("json", models.MyModel.objects.all())
out  = open("mymodel.json", "w")
out.write(data)
out.close()
