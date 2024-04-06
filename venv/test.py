from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()


class User_Test(TestCase):

    def setUp(self):
        
        
        #User.query.delete()
        Post.query.delete()
       

        William = User(First_Name='William',Last_Name='Gonzales',Profile_Pic='https://publish-p47754-e237306.adobeaemcloud.com/adobe/dynamicmedia/deliver/dm-aid--e7154f9f-8a49-4afb-a8f1-278d54ae6a76/_330587629904.app.png?preferwebp=true&width=420')
        post1= Post(title="First Post", comment='First comment', user_ref = 1)
        db.session.add(post1)
        db.session.add(William)
        db.session.commit()

        self.user_id = William.user_id
        self.post_id=post1.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_Home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('William', html)

    def test_details(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('William', html)

    def test_create_user(self):
        with app.test_client() as client:
            Juan = {'First_Name':'Juan', 'Last_Name':'Jimenes', 'Profile_Pic':'https://publish-p47754-e237306.adobeaemcloud.com/adobe/dynamicmedia/deliver/dm-aid--323b5cf8-c89f-4158-addd-80b45571ff09/_383195890566.app.png?preferwebp=true&width=420'}
            resp = client.post('/user_create', data=Juan, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>First Name: Juan</li>', html)
            
    def test_edit_user(self):
        with app.test_client() as client:
            Juan = {'id':self.user_id, 'First_Name':'Juan', 'Last_Name':'Jimenes', 'Profile_Pic':'https://publish-p47754-e237306.adobeaemcloud.com/adobe/dynamicmedia/deliver/dm-aid--323b5cf8-c89f-4158-addd-80b45571ff09/_383195890566.app.png?preferwebp=true&width=420'}
            resp = client.post('/edit', data=Juan, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Juan', html)

    def test_Post_Details(self):
        with app.test_client() as client:
            resp = client.get(f"/p{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Post', html)
          
    def test_edit_post(self):
        with app.test_client() as client:
            post3 = {'id':self.post_id ,'title':'third','comment':'third Comment','user_ref':self.user_id}
            resp = client.post('/edit_post', data=post3, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('third', html)                
    
    def test_User_Post(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First', html)        