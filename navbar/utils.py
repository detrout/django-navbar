from __future__ import absolute_import
from six import iteritems

from .settings import CACHE_PREFIX


def _Qperm(user=None):
    from django.db.models.query import Q
    exQ = Q()
    if user is None or user.is_anonymous():
        exQ = (Q(user_type__exact='A') | Q(user_type__exact='E')) & Q(
            groups__isnull=True)
    elif user.is_superuser:
        exQ = ~Q(user_type__exact='A')
    elif user.is_staff:
        exQ = (Q(user_type__exact='E') | Q(user_type__exact='L') |
               Q(user_type__exact='S')) & (
                    Q(groups__in=user.groups.all()) | Q(groups__isnull=True))
    else:
        exQ = (Q(user_type__exact='E') | Q(user_type__exact='L')) & (
                    Q(groups__in=user.groups.all()) | Q(groups__isnull=True))
    return exQ


def generate_navtree(user=None, maxdepth=-1):
    from .models import NavBarEntry
    if maxdepth == 0:
        return []  # silly...
    permQ = _Qperm(user)
    urls = {}

    def navent(ent, invdepth, parent):
        current = {
            'name': ent.name,
            'title': ent.title,
            'url': ent.url,
            'selected': False,
            'path_type': ent.path_type,
            'parent': parent,
        }
        urls.setdefault(ent.url, current)
        current['children'] = navlevel(ent.children, invdepth - 1, current)
        return current

    def navlevel(base, invdepth, parent=None):
        if invdepth == 0:
            return []
        return [navent(ent, invdepth, parent)
                        for ent in base.filter(active=True).filter(permQ).distinct().order_by('order')]
    tree = navlevel(NavBarEntry.top, maxdepth)
    urls = sorted(iteritems(urls), key=lambda x: x[0], reverse=True)
    return {'tree': tree, 'byurl': urls}


def get_navtree(user=None, maxdepth=-1):
    from django.core.cache import cache
    cachename = '%s_site_navtree' % CACHE_PREFIX
    timeout = 60 * 60 * 24
    if user is not None and not user.is_anonymous():
        if user.is_superuser:
            cachename = '%s_site_navtree_super' % CACHE_PREFIX
        else:
            cachename = 'site_navtree_' + str(user.id)
            timeout = 60 * 15
    data = cache.get(cachename)
    if data is None:
        data = generate_navtree(user, maxdepth)
        cache.set(cachename, data, timeout)
    return data


def get_navbar(user=None):
    from .models import NavBarEntry
    return NavBarEntry.top.filter(_Qperm(user))
