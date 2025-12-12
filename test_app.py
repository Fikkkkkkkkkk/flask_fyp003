import unittest
from main import app, db, Item

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        response = self.app.post('/create', data=dict(name='Test Item', description='Test Desc'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Item', response.data)

    def test_edit_item(self):
        with app.app_context():
            item = Item(name='Old Name', description='Old Desc')
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        response = self.app.post(f'/edit/{item_id}', data=dict(name='New Name', description='New Desc'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Name', response.data)

    def test_delete_item(self):
        with app.app_context():
            item = Item(name='Delete Me', description='Desc')
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        response = self.app.post(f'/delete/{item_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Me', response.data)

if __name__ == '__main__':
    unittest.main()
