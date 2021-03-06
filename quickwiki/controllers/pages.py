import logging
from cgi import escape

from pylons import url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.decorators.secure import authenticate_form

from quickwiki.lib.base import BaseController, render
from quickwiki.lib.helpers import flash
from quickwiki.model import Page, wikiwords
from quickwiki.model.meta import Session

log = logging.getLogger(__name__)

class PagesController(BaseController):
    
    def __before__(self):
        self.page_q = Session.query(Page)
    
    def show(self, title):
        page = self.page_q.filter_by(title=title).first()
        c.title = title
        if page:
            c.content = page.get_wiki_content()
            return render('/pages/show.mako')
        elif wikiwords.match(title):
            return render('/pages/new.mako')
        abort(404)
    
    def edit(self, title):
        c.title = title
        c.content = u''
        page = self.page_q.filter_by(title=title).first()
        if page:
            c.title = page.title
            c.content = page.content
        return render('/pages/edit.mako')
    
    @authenticate_form
    def save(self, title):
        c.title = title
        page = self.page_q.filter_by(title=title).first()
        if not page:
            page = Page(title=title)
        # In a real application, you should validate and sanitize
        # submitted data throughly! escape is a minimal example here
        page.content = escape(request.POST.getone('content'))
        Session.add(page)
        Session.commit()
        flash('Successfully saved %s!' % title)
        redirect(url('show_page', title=title))
    
    def index(self):
        c.titles = [page.title for page in self.page_q.all()]
        return render('/pages/index.mako')
    
    @authenticate_form
    def delete(self):
        titles = request.POST.getall('title')
        pages = self.page_q.filter(Page.title.in_(titles))
        for page in pages:
            Session.delete(page)
        Session.commit()
        # flash only after a successful commit
        for title in titles:
            flash('Deleted %s.' % title)
        redirect(url('pages'))
    

