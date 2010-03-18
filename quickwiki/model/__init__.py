"""The application's model objects"""
import logging
import re
import sys
if sys.version < 2.6:
    import sets.Set as set
from docutils.core import publish_parts
from sqlalchemy import orm, Column, Unicode, UnicodeText
from quickwiki.lib.helpers import url, link_to
from quickwiki.model.meta import Session, Base

log = logging.getLogger(__name__)
# disable docutils security hazards:
# http://docutils.sourceforge.net/docs/howto/security.html
SAFE_DOCUTILS = dict(file_insertion_enabled=False, raw_enabled=False)
wikiwords = re.compile(r'\b([A-Z]\w+[A-Z]+\w+)', re.UNICODE)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)


class Page(Base):
    __tablename__ = 'pages'
    title = Column(Unicode(40), primary_key=True)
    content = Column(UnicodeText(), default=u'')
    
    @orm.validates('title')
    def validate_title(self, key, title):
        """Assure that page titles are wikiwords and valid length"""
        if len(title) > 40:
            raise ValueError('Page title must be 40 characters or fewer')
        if not wikiwords.match(title):
            log.warning('%s: invalid title (%s)' % (self.__class__.__name__,
                                                    title))
            raise ValueError('Page title must be a wikiword (CamelCase)')
        return title
    
    def get_wiki_content(self):
        """Convert reStructuredText content to HTML for display, and
        create links for WikiWords
        """
        content = publish_parts(self.content, writer_name='html',
                                settings_overrides=SAFE_DOCUTILS)['html_body']
        titles = set(wikiwords.findall(content))
        for title in titles:
            title_url = url(controller='pages', action='show', title=title)
            content = content.replace(title, link_to(title, title_url))
        return content
    
    def __unicode__(self):
        return self.title
    
    def __repr__(self):
        return "<Page('%s', '%s')>" % (self.title, self.content)
    
    __str__ = __unicode__
    
