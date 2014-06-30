from requests import request, HTTPError
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from apps.auth.exceptions import EmailExists

USER_MODEL = get_user_model()

def save_profile_picture(strategy, user, response, details,
                         is_new=False,*args,**kwargs):

    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            user.picture.save('{0}_fb_social.jpg'.format(user.username),
                                   ContentFile(response.content))
            user.save()


def get_extra_facebook_data(strategy, user, response, details, is_new=False, *args, **kwargs):
    #TODO: Load more relevant Facebook data to our profile if necessary
    pass


def verify_email(strategy, user, request, **kwargs):
    """ Raise a custom exception if the email address already exists"""
    #TODO: Left here because we may need to implement something like this in the near future


    if not kwargs['is_new']:
        return

    try:
        user = USER_MODEL.objects.get(email=kwargs['details']['email'])
        raise EmailExists
    except USER_MODEL.DoesNotExist:
        pass
