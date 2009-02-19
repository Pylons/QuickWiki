from quickwiki.tests import *

class TestPagesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pages', action='index'))
        self.assert_('Title List' in response)
        self.assert_('FrontPage' in response)
