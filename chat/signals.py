import json
import channels.layers
from asgiref.sync import async_to_sync

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


def chat_message(event):
    '''
    Call back function to send message to the browser
    '''
    message = event['message']
    channel_layer = channels.layers.get_channel_layer()
    # Send message to WebSocket
    async_to_sync(channel_layer.send)(text_data=json.dumps(
        message
    ))


@receiver(post_save, sender=Message, dispatch_uid='msg_status_listeners')
def update_job_status_listeners(sender, instance, **kwargs):
    group_name = instance.room.name

    message = {
        'message_id': instance.id,
        'text': instance.text
    }

    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'chat_message',
            'message': message
        }
    )
