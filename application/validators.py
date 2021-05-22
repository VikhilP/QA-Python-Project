from wtforms.fields.core import IntegerField
from application import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField, DateField
from wtforms.validators import *
from application.models import *

# class UniqueValidator(object):
#     def __init__(self, model, field, message=None):
#         self.model = model
#         self.field = field
#         if not message:
#             message = 'This item already exists'
#         self.message = message

#     def __call__(self, form, field):
        
#         if field.object_data == field.data:
#             return
#         check = GameSeries.query.filter_by(field == data).first()
#         if check:
#             raise ValidationError(self.message)

# class Unique(object):
#     def __init__(self, model, field, message='Should be Unique'):
#         self.model = model
#         self.field = field

#     def __call__(self, form, field):
#         if not field.data:
#             check = self.model.query.filter(self.field == field.data).first()
#             if check:
#                 raise ValidationError(self.message)
#         raise ValidationError(message='Should not be blank')

# class UserCheck:
#     def __init__(self, banned, message=None):
#         self.banned = banned
#         if not message:
#             message = 'This item already exists'
#         self.message = message

#     def __call__(self, form, field):
#         if field.data in self.banned:
#             raise ValidationError(self.message)