from django.db import models
from django.utils import timezone

# Create your models here.
class Message(models.Model):
    username = models.CharField(max_length=250)
    msg_type = models.CharField(max_length=2, choices=(('1','Login Message'),('2','Logout Message'),('0','Chat')), default = 0)
    message = models.TextField(blank=True, null = True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_message(self):
        if self.msg_type == '1':
            return str('<p class="mb-0 text-center text-muted"><b>' + self.username + '</b> joined the conversation</p>')
        elif self.msg_type == '2':
            return str('<p class="mb-0 text-center text-muted"><b>' + self.username + '</b>  has left the room</p>')
        else:
            message = (self.message).replace("\n","<br>")
            return str('<div class="d-flex w-100"><div class="col-auto pe-2"><b>' + self.username + ":</b></div><div class='col-auto flex-shrink flex-grow-1 w-min-content mb-0'><p>" + message+"</p></div></div>")

