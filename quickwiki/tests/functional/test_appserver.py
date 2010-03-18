from quickwiki.tests import *

class TestAppServer(TestController):
    def test_index(self):
        response = self.app.get('/')
        # Test response...
        assert 'front page!' in response
