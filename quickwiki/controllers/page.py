from quickwiki.lib.base import *
    
class PageController(BaseController):

    def __before__(self):
        model.session_context.current.clear()

    def index(self, title):
        page = model.Page.get_by(title=title)
        if page: 
            c.content = page.get_wiki_content()
            return render_response('/page.myt')
        elif model.wikiwords.match(title):
            return render_response('/new_page.myt')
        abort(404)

    def edit(self, title):
        page = model.Page.get_by(title=title)
        if page:
            c.content = page.content
        return render_response('/edit.myt')
    
    def save(self, title):
        page = model.Page.get_by(title=title)
        if not page:
            page = model.Page()
            page.title = title
        page.content = request.params['content']
        c.title = page.title
        c.content = page.get_wiki_content()
        c.message = 'Successfully saved'
        page.flush()
        return render_response('/page.myt')

    def list(self):
        c.titles = [page.title for page in model.Page.select()]
        return render_response('/titles.myt')

    def delete(self):
        title = request.params['id'][5:]
        page = model.Page.get_by(title=title)
        page.delete()
        page.flush()
        c.titles = model.Page.select()
        return render_response('/list.myt', fragment=True)
