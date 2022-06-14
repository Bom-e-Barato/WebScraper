from rest_framework import serializers

from conversation.models import Conversation

class AddConversationSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Conversation
        fields = ('sender', 'receiver', 'message')

    def save(self):
        conversation = Conversation(**self.validated_data)
        conversation.save()
        return conversation

class ShowConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        

 
        