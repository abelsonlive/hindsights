#!/usr/bin/python
# -*- coding: utf-8 -*-
import facepy
import yaml
from datetime import datetime, timedelta
from urlparse import parse_qs

def generate_extended_access_token(conf="config.yml"):
    """
    Get an extended OAuth access token.

    :param access_token: A string describing an OAuth access token.
    :param application_id: An integer describing the Facebook application's ID.
    :param application_secret_key: A string describing the Facebook application's secret key.

    Returns a tuple with a string describing the extended access token and a datetime instance
    describing when it expires.
    """
    # Configuration
    c = yaml.safe_load(open(conf))
    app_id = c['fb_app_id']
    app_secret = c['fb_app_secret']
    temp_access_token = c['fb_temp_access_token']

    # access tokens
    default_access_token = facepy.get_application_access_token(
        application_id=app_id,  
        application_secret_key=app_secret
    )
    graph = facepy.GraphAPI(default_access_token)

    response = graph.get(
        path='oauth/access_token',
        client_id=app_id,
        client_secret=app_secret,
        grant_type='fb_exchange_token',
        fb_exchange_token=temp_access_token
    )

    components = parse_qs(response)

    token = components['access_token'][0]
    expires_at = datetime.now() + timedelta(seconds=int(components['expires'][0]))

    c['fb_stable_access_token'] = token
    c['fb_stable_access_token_expires_at'] = expires_at.strftime("%Y-%m-%d %H:%M:%S")
    
    with open(conf, 'wb') as f:
        f.write(yaml.dump(c))
    print "HERE IS YOUR STABLE ACCESS TOKEN: %s" % token
    print "IT EXPIRES AT %s" % expires_at
    print "YOU CONFIG FILE (%s) HAS BEEN UPDATED" % conf

def connect(conf="config.yml"):
    c = yaml.safe_load(open(conf))
    return facepy.GraphAPI(c['fb_stable_access_token'])

if __name__ == '__main__':
    generate_extended_access_token()
    