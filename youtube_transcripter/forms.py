from django import forms

class YoutubeForm(forms.Form):
    video_link = forms.CharField(label='Youtube Link', max_length=1000)