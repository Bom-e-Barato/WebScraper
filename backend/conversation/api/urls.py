from django.urls import path
from conversation.api.views import(
    add_message_view,
    get_conversation_view

)

app_name = "conversation"

urlpatterns = [
    path("add_message", add_message_view, name="add_message"),
    path("conversation_with/<int:id>", get_conversation_view, name="my_conversation"),
]