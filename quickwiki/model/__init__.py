"""The application's model objects"""
import logging
import re
import sets
from docutils.core import publish_parts

import sqlalchemy as sa
from sqlalchemy import orm

from pylons import url
from quickwiki.model import meta
import quickwiki.lib.helpers as h


docutils_safety = {'file_insertion_enabled': False, 'raw_enabled': False}
log = logging.getLogger(__name__)
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)", re.UNICODE)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    sm = orm.sessionmaker(bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)


pages_table = sa.Table('pages', meta.metadata,
    sa.Column('title', sa.types.Unicode(40), primary_key=True),
    sa.Column('content', sa.types.Unicode(), default='')
)

class Page(object):
    content = None

    def __str__(self):
        return self.title

    @orm.validates('title')
    def validate_title(self, key, title):
        """Assure that page titles are wikiwords"""
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
                                settings_overrides=docutils_safety)['html_body']
        titles = sets.Set(wikiwords.findall(content))
        for title in titles:
            title_url = url(controller='pages', action='show', title=title)
            content = content.replace(title, h.link_to(title, title_url))
        return content

orm.mapper(Page, pages_table)
