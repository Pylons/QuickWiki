import re
import sets
from docutils.core import publish_parts
from sqlalchemy import *
from sqlalchemy.ext.assignmapper import assign_mapper
from pylons.database import session_context
import quickwiki.lib.helpers as h

wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

meta = DynamicMetaData()

pages_table = Table('pages', meta,
    Column('title', String(40), primary_key=True),
    Column('content', String(), default='')
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
        
page_mapper = assign_mapper(session_context, Page, pages_table)
