from quickwiki.tests import *
from quickwiki.tests import Session, Page, TestController

class TestPages(TestController):
    
    def test_index(self):
        q1 = Session.query(Page).all()
        assert len(q1) == 1
        page = Page()
        page.title = u'TestPage'
        page.content = u'Welcome to the QuickWiki test page.'
        Session.add(page)
        Session.commit()
        q2 = Session.query(Page).all()
        print(q2)
        assert q2 == [q1[0], page]
    

