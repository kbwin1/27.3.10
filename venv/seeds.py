from models import User, db, Post, Tag, PostTag
from app import app

## CREATE ALL TABLES
db.drop_all()
db.create_all()

#IF table isnt empty empty it all
User.query.delete()

#add data 
William = User(First_Name='William',Last_Name='Gonzales',Profile_Pic='https://publish-p47754-e237306.adobeaemcloud.com/adobe/dynamicmedia/deliver/dm-aid--e7154f9f-8a49-4afb-a8f1-278d54ae6a76/_330587629904.app.png?preferwebp=true&width=420')
Juan = User(First_Name='Bowser', Last_Name='Jimenes', Profile_Pic='https://publish-p47754-e237306.adobeaemcloud.com/adobe/dynamicmedia/deliver/dm-aid--323b5cf8-c89f-4158-addd-80b45571ff09/_383195890566.app.png?preferwebp=true&width=420')
Pedro = User(First_Name='Pedro', Last_Name='Gomez', Profile_Pic='https://publish-p47754-e237306.adobeaemcloud.com/adobe/dynamicmedia/deliver/dm-aid--503de83a-62df-4c8a-b047-bedb22002ae4/_405531873648.app.png?preferwebp=true&width=420')

post1= Post(title="First Post", comment='First comment', user_ref = 1)
post2= Post(title="Second Post", comment='Second comment', user_ref = 2)
#add new object to session so they will saty

tag1=Tag(name="Fun")
post_tag_1=PostTag(post_id=1,tag_id=1)


db.session.add(William)
db.session.add(Juan)
db.session.add(Pedro)

db.session.commit()

db.session.add(post1)

db.session.commit()

db.session.add(tag1)

db.session.commit()

db.session.add(post_tag_1)

db.session.commit()


