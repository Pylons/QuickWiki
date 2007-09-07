import logging

from quickwiki.lib.base import *
from quickwiki.model import Session, Page

log = logging.getLogger(__name__)

class PageController(BaseController):
    
    def index(self, title):
        page_q = Session.query(Page)
        page = page_q.filter_by(title=title).first()
        if page:
            c.content = page.get_wiki_content()
            return render('/page.mako')
        elif model.wikiwords.match(title):
            return render('/new_page.mako')
        abort(404)

    def edit(self, title):
        page_q = Session.query(Page)
        page = page_q.filter_by(title=title).first()
        if page:
            c.content = page.content
        return render('/edit.mako')
        
    def save(self, title):
        page_q = Session.query(Page)
        page = page_q.filter_by(title=title).first()
        if not page:
            page = Page()
            page.title = title
        page.content = request.params.get('content','')
        c.title = page.title
        c.content = page.get_wiki_content()
        c.message = 'Successfully saved'
        Session.save(page)
        Session.commit()
        return render('/page.mako')

    def list(self):
        c.titles = [page.title for page in Session.query(Page).all()]
        return render('/list.mako')

    def delete(self):
        page_q = Session.query(Page)
        title = request.params['id'][5:]
        page = page_q.filter_by(title=title).one()
        Session.delete(page)
        Session.commit()
        c.titles = page_q.all()
        return render('/list-titles.mako')
