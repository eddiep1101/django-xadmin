#coding:utf-8
from __future__ import print_function
import httplib2
from django.template import loader
from django.core.cache import cache
from django.utils import six
from django.utils.translation import ugettext as _
from django.conf import settings

from xadmin.sites import site
from xadmin.models import UserSettings
from xadmin.views import BaseAdminPlugin, BaseAdminView
from xadmin.util import static, json
import six
if six.PY2:
    import urllib
else:
    import urllib.parse

THEME_CACHE_KEY = 'xadmin_themes'


class ThemePlugin(BaseAdminPlugin):

    enable_themes = False
    # {'name': 'Blank Theme', 'description': '...', 'css': 'http://...', 'thumbnail': '...'}
    user_themes = None
    use_bootswatch = False
    default_theme = static('xadmin/css/themes/bootstrap-xadmin.css')
    bootstrap2_theme = static('xadmin/css/themes/bootstrap-theme.css')

    def init_request(self, *args, **kwargs):
        return self.enable_themes

    def _get_theme(self):
        if self.user:
            try:
                return UserSettings.objects.get(user=self.user, key="site-theme").value
            except Exception:
                pass
        if '_theme' in self.request.COOKIES:
            if six.PY2:
                func = urllib.unquote
            else:
                func = urllib.parse.unquote
            return func(self.request.COOKIES['_theme'])
        return self.default_theme

    def get_context(self, context):
        context['site_theme'] = self._get_theme()
        return context

    # Media
    def get_media(self, media):
        return media + self.vendor('jquery-ui-effect.js', 'xadmin.plugin.themes.js')

    # Block Views
    def block_top_navmenu(self, context, nodes):

        themes = [
            {'name': _(u"Default"), 'description': _(u"Default bootstrap theme"), 'css': self.default_theme},
            {'name': _(u"Bootstrap2"), 'description': _(u"Bootstrap 2.x theme"), 'css': self.bootstrap2_theme},
            ]
        select_css = context.get('site_theme', self.default_theme)

        if self.user_themes:
            themes.extend(self.user_themes)

        if self.use_bootswatch:
            ex_themes = cache.get(THEME_CACHE_KEY)
            if ex_themes:
                themes.extend(json.loads(ex_themes))
            else:
                ex_themes = []
<<<<<<< HEAD

                use_local_watch_themes = getattr(settings, 'USE_LOCAL_WATCH_THEMES', False)

                try:                    
                    if use_local_watch_themes:
                        # fetching themes from local web server
#                         requesting_host = self.request.get_host() or ''
#                         print requesting_host
                        watch_themes_str = urllib.urlopen(self.request.build_absolute_uri('/static/xadmin/vendor/bootswatch/api.bootswatch.com.3')).read()
# 
                        from django.template import Context, Template
                        watch_themes_template = Template(watch_themes_str)
                        watch_themes_str = watch_themes_template.render(Context())
                        
                    else:
                        # fetching themes from bootswatch
                        h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
                        resp, watch_themes_str = h.request("http://bootswatch.com/api/3.json", 'GET', \
                            "", headers={"Accept": "application/json", "User-Agent": self.request.META['HTTP_USER_AGENT']})

#                     print watch_themes_str

                    watch_themes = json.loads(watch_themes_str)['themes']
=======
                try:
                    h = httplib2.Http()
                    resp, content = h.request("http://bootswatch.com/api/3.json", 'GET', '',
                        headers={"Accept": "application/json", "User-Agent": self.request.META['HTTP_USER_AGENT']})
                    if six.PY3:
                        content = content.decode()
                    watch_themes = json.loads(content)['themes']
>>>>>>> 5d0dd31291aee2d9679b372cbecf5bc5f07c52b0
                    ex_themes.extend([
                        {'name': t['name'], 'description': t['description'],
                            'css': t['cssMin'], 'thumbnail': t['thumbnail']}
                        for t in watch_themes])
<<<<<<< HEAD

                except Exception, e:
                    print unicode(e)
=======
                except Exception as e:
                    print(e)
>>>>>>> 5d0dd31291aee2d9679b372cbecf5bc5f07c52b0

                cache.set(THEME_CACHE_KEY, json.dumps(ex_themes), 24 * 3600)
                themes.extend(ex_themes)

        nodes.append(loader.render_to_string('xadmin/blocks/comm.top.theme.html', {'themes': themes, 'select_css': select_css}))


site.register_plugin(ThemePlugin, BaseAdminView)