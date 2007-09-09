from quickwiki.tests import *

class TestPageController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='page'))
        # Test response...
