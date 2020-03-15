import mongoengine


class Video(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    theme = mongoengine.StringField(required=True)
    thumbs_up = mongoengine.IntField(default=0)
    thumbs_down = mongoengine.IntField(default=0)

