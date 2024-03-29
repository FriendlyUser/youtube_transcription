from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from youtube_transcripter.forms import YoutubeForm
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def transcript_json(request):
  video_id = request.GET['video_link']
  transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
  transcript = transcript_list.find_transcript(['en-US', 'en'])
  full_transcript = transcript.fetch()
  return JsonResponse({"transcript": full_transcript})

def get_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YoutubeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            if request.POST['video_link']:
                # grab video transcript
                video_param = request.POST['video_link']
                parsed_url = urlparse(video_param)
                if parsed_url.query is "":
                  video_id = video_param
                else:
                  url_params = parse_qs(parsed_url.query)
                  video_id = url_params.get('v')[0]
                  print(video_id)
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript(['en-US', 'en'])
                full_transcript = transcript.fetch()
                return render(request, 'transcript.html', {'transcript_items': full_transcript}) 
                # return template with transcript and copiable json object?
            return HttpResponseRedirect('/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = YoutubeForm()

    return render(request, 'form.html', {'form': form})


def render_thanks(request):
    return HttpResponse("Thank You")