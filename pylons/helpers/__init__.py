#from decorator import decorator
from math import ceil
from pylons import request, url


class Paginator:
    def __init__(self, page=None, limit=None, width=None, items_count=0):
        self.page = int(page or request.params.get('pag_page', 1))
        self.limit = int(limit or request.params.get('pag_limit', 2))
        self.width = int(width or request.params.get('pag_width', 0))
        self.items_count = int(items_count)
        self.params = None

    def get_range(self, **kargs):
        try:
            self.page = int(kargs.get('page', self.page))
            self.limit = int(kargs.get('limit', self.limit))
        except:
            pass
        return ((self.page-1)*self.limit, 
            self.page*self.limit, self.limit)

    def get_pages_count(self):
        return int(ceil(float(self.items_count) / self.limit)) or 1

    def create_params(self):
        pars = dict(pag_width=self.width, pag_limit=self.limit)
        pars.update(request.params)
        params = list()
        for key, val in pars.iteritems():
            params.append('%s=%s' % (key, val))

        self.params = '&'.join(params)

    def pages(self):
        count = self.get_pages_count()
        pages = list()

        start = self.page - self.width
        end = self.page + self.width

        if start < 1:
            start = 1
        if end > count:
            end = count

        for i in range(start, end + 1):
            link = ['?' + self.params + '&pag_page=%s' % i, i]
            pages.append(link)

        return pages

    def before_sep(self):
        return self.page - self.width > 2

    def after_sep(self):
        return self.page + self.width < self.get_pages_count() - 1

    def previous(self):
        if self.page > 1:
            return ('?' + self.params + '&pag_page=%s' % (self.page-1),
                self.page-1)
        else:
            return None 

    def next(self):
        if self.page < self.get_pages_count():
            return ('?' + self.params + '&pag_page=%s' % (self.page+1),
                self.page+1)
        else:
            return None 

    def first(self):
        if self.page - self.width > 1:
            return '?' + self.params + '&pag_page=1'
        else:
            return None

    def last(self):
        count = self.get_pages_count()
        if self.page + self.width < count:
            return '?' + self.params + '&pag_page=%s' % count
        else:
            return None

#def paginate(collection, page=1, width=2):
#    def decorate(f, *args, **kargs):
#        self = args[0]
#        page = request.params.get('page', 1)
#   
#        items = getattr(c._current_obj, collection, None)
#        print '#ITEMS:', items

#        pag = []
#        c.paginator = pag

#        output = f(*args, **kargs)
#        return output
#    return decorator(decorate)
