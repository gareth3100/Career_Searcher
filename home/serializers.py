from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    #need to specify all fields in your model
    class Meta:
        model = Article
        #fields = ['id', 'title', 'author', 'email'] #if you add stuff, it appears on the JSON query
        fields = '__all__'

    
        