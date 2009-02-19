"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

import logging
import re
import sets
from docutils.core import publish_parts

from pylons import url
from quickwiki.lib.helpers import link_to
from quickwiki.model import meta


log = logging.getLogger(__name__)
SAFE_DOCUTILS = {'file_insertion_enabled': False, 'raw_enabled': False}
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)", re.UNICODE)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine


pages_table = sa.Table('pages', meta.metadata,
    sa.Column('title', sa.types.Unicode(40), primary_key=True),
    sa.Column('content', sa.types.Unicode(), default='')
)

class Page(object):
    def __init__(self, title, content=None):
        self.title = title
        self.content = content

    @orm.validates('title')
    def validate_title(self, key, title):
        """Assure that page titles are wikiwords and valid length."""
        if len(title) > 40:
            raise ValueError("Page title must be 40 characters or fewer")
        if wikiwords.match(title) is None:
            log.warning("%s: invalid title (%s)" % (self.__class__.__name__,
                                                    title))
            raise ValueError("Page title must be a wikiword (CamelCase)")
        return title

    def get_wiki_content(self):
        """Convert reStructuredText content to HTML for display, and
        create links for WikiWords.
        """
        content = publish_parts(self.content, writer_name='html',
                                settings_overrides=SAFE_DOCUTILS)['html_body']
        titles = sets.Set(wikiwords.findall(content))
        for title in titles:
            title_url = url(controller='pages', action='show', title=title)
            content = content.replace(title, link_to(title, title_url))
        return content

    def __unicode__(self):
        return self.title

    __str__ = __unicode__
    
    def __repr__(self):
        return "<Page('%s', '%s')>" % (self.title, self.content)

orm.mapper(Page, pages_table)
