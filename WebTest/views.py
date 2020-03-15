import json

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from mongoengine import connect

from WebTest.forms import VideoForm
from WebTest.models import Video
from WebTest.settings import DATABASES


class MongoDataBaseView:

    def __init__(self, db_info):
        self.database = db_info

    def connect(self):
        return connect(
            self.database.get('DBNAME'),
            host=self.database.get('host'),
            port=self.database.get('port'),
            username=self.database.get('username'),
            password=self.database.get('password'),
            retryWrites=False
        )


class HomeView(View, MongoDataBaseView):
    form_class = VideoForm
    success_url = reverse_lazy('home_page')
    template_name = 'home-page.html'
    database = DATABASES.get('mongodb')
    MongoDataBaseView(database)

    def get(self, request, *args, **kwargs):

        self.connect()

        form = self.form_class()

        context = {
            'videos': Video.objects(),
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = VideoForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            self.save(request, data)

            self.connect()

            form = self.form_class()

            context = {
                'videos': Video.objects(),
                'form': form
            }

            return render(request, self.template_name, context)

        self.connect()

        context = {
            'videos': Video.objects(),
            'form': form
        }

        return render(request, self.template_name, context)

    def save(self, request, data):
        self.connect()
        video = Video(
            name=data['name'],
            theme=data['theme']
        )
        video.save()


class ThumbUpView(View, MongoDataBaseView):
    success_url = reverse_lazy('home_page')
    template_name = 'home-page.html'
    database = DATABASES.get('mongodb')
    MongoDataBaseView(database)

    def get(self, request, *args, **kwargs):

        self.connect()

        video = Video.objects(id=kwargs.get('id')).first()
        video.thumbs_up += 1
        video.save()

        return HttpResponse(json.dumps({
            "status": "success",
            "message": "Thumb Up",
            "ThumbUp": video.thumbs_up
        }), content_type="application/json")


class ThumbDownView(View, MongoDataBaseView):
    success_url = reverse_lazy('home_page')
    template_name = 'home-page.html'
    database = DATABASES.get('mongodb')
    MongoDataBaseView(database)

    def get(self, request, *args, **kwargs):

        self.connect()

        video = Video.objects(id=kwargs.get('id')).first()
        video.thumbs_down += 1
        video.save()

        return HttpResponse(json.dumps({
            "status": "success",
            "message": "Thumb Down",
            "ThumbDown": video.thumbs_down
        }), content_type="application/json")


class ListThemesView(View, MongoDataBaseView):
    success_url = reverse_lazy('home_page')
    template_name = 'list.html'
    database = DATABASES.get('mongodb')
    MongoDataBaseView(database)

    def get(self, request, *args, **kwargs):

        self.connect()

        pipeline = [
          {
            '$group': {'_id': '$theme', 'thumbs_up': {'$sum': '$thumbs_up'}, 'thumbs_down': {'$sum': '$thumbs_down'}}
          },
          {
            '$project': {'name': '$_id', 'score': {
                    '$subtract': [
                        '$thumbs_up',
                        {
                            '$divide': ['$thumbs_down', 2]
                        }
                    ]
                }
            }
          },
          {'$sort': {'score': -1}}
        ]

        themes = list(Video.objects().aggregate(pipeline))

        context = {
            'themes': themes
        }
        return render(request, self.template_name, context)
