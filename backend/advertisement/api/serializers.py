from rest_framework import serializers

from advertisement.models import Advertisement

class AddAdvertisementSerializer(serializers.ModelSerializer):
    img       = serializers.ImageField(allow_null=True, required=False)
    promoted    = serializers.BooleanField(required=False)
    negotiable  = serializers.BooleanField(required=False)
    category    = serializers.CharField(max_length=20, allow_null=True, required=False)
    location    = serializers.CharField(max_length=100,required=False)
    class Meta:
        model = Advertisement
        fields = ('name', 'img', 'price', 'description', 'promoted', 'negotiable', 'category', 'location')

    def save(self):
        advertisement = Advertisement(**self.validated_data)
        advertisement.save()
        return advertisement

class ShowAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        exclude = ['date_created']



        
