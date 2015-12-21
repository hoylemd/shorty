import os
import shorty
import unittest
import tempfile


class ShortyTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, shorty.app.config['DATABASE'] = tempfile.mkstemp()
        shorty.app.config['TESTING'] = True
        self.app = shorty.app.test_client()
        shorty.init_db()

    def tearDown(self):
        import pdb; pdb.set_trace()
        os.close(self.db_fd)
        os.unlink(shorty.app.config['DATABASE'])

    def test_create_url__google(self):
        rv = self.app.post('/', data={'url': 'www.google.com'})
        import pdb; pdb.set_trace()
        assert len(rv.data) > 0

if __name__ == '__main__':
    unittest.main()
