import re
import sets

from docutils.core import publish_parts
from pylons import config
from sqlalchemy import Column, MetaData, Table, types
from sqlalchemy.orm import mapper
from sqlalchemy.orm import scoped_session, sessionmaker

import quickwiki.lib.helpers as h

# Global session manager for SQLAlchemy. Session() returns the session
# object appropriate for the current web request.
Session = scoped_session(sessionmaker(autoflush=True, transactional=True,
                                      bind=config['pylons.g'].sa_engine))

# Global metadata. If you have multiple databases with overlapping
# table names, you'll need a metadata for each database.
metadata = MetaData()

wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)", re.UNICODE)

pages_table = Table('pages', metadata,
    Column('title', types.Unicode(40), primary_key=True),
    Column('content', types.Unicode(), default='')
)

class Page(object):
    content = None

    def __str__(self):
        return self.title

    def get_wiki_content(self):
        content = publish_parts(self.content, writer_name="html")["html_body"]
        titles = sets.Set(wikiwords.findall(content))
        for title in titles:
            title_url = h.url_for(controller='page', action='index',
                                  title=title)
            content = content.replace(title, h.link_to(title, title_url))
        return content

mapper(Page, pages_table)
