from django.db import models
from core      import models as core_models


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField('users.User', blank=True)

    def __str__(self):
        # usernames = []
        # for user in self.participants.all():
        #     usernames.append(user.name)

        usernames = [user.username for user in self.participants.all() ]

        return ', '.join(usernames) 

    def count_messages(self):
        return self.messages.count()
    count_messages.short_description = 'Number of Messages'

    def count_participants(self):
        return self.participants.count()
    count_participants.short_description = 'Number of Participants'

    class Meta:
        db_table = 'conversations'


class Message(core_models.TimeStampedModel):

    message      = models.TextField()
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages',null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages',null=True)

    def __str__(self):
        return f"{self.user} says: {self.message}"
    
    class Meta:
        db_table = 'messages'