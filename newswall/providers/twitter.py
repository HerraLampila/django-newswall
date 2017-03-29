"""
Twitter API Feed Provider
=========================

---

Required: tweepy

pip install tweepy

---

Usage:

Create a twitter app.
You'll find the consumer_key/secret on the detail page.
Because this is a read-only application, you can create
your oauth_token/secret directly on the bottom of the app detail page.

---

Required configuration keys::

    {
    "provider": "newswall.providers.twitter",
    "user": "feinheit",
    "consumer_key": "...",
    "consumer_secret": "...",
    "oauth_token": "...",
    "oauth_secret": "..."
    }

"""
import tweepy

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        auth = tweepy.OAuthHandler(
            self.config['consumer_key'],
            self.config['consumer_secret']
        )

        auth.set_access_token(
            self.config['oauth_token'],
            self.config['oauth_secret']
        )

        api = tweepy.API(auth)
        entries = api.user_timeline(screen_name=self.config['user'])

        for entry in entries:
            media_url = entry.entities.get('media', [{}, ])[0].get(
                'media_url_https', '')
            link = 'http://twitter.com/%s/status/%s' % (
                self.config['user'],
                entry.id,
            )

            self.create_story(
                link,
                image_url=media_url,
                title=entry.id,
                body=entry.text,
                timestamp=entry.created_at,
            )
