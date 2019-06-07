from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///catalogue.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="dummy user", email="dummy@example.com",
             picture='')
session.add(User1)
session.commit()

# Categories
category1 = Category(user_id=1, title="Soccer")

session.add(category1)
session.commit()

category2 = Category(user_id=1, title="Basketball")

session.add(category2)
session.commit()

category3 = Category(user_id=1, title="Baseball")

session.add(category3)
session.commit()

category4 = Category(user_id=1, title="Frisbee")

session.add(category4)
session.commit()

category5 = Category(user_id=1, title="Snowboarding")

session.add(category5)
session.commit()

category6 = Category(user_id=1, title="Rock Climbing")

session.add(category6)
session.commit()

category7 = Category(user_id=1, title="Foosball")

session.add(category7)
session.commit()

category8 = Category(user_id=1, title="Skating")

session.add(category8)
session.commit()

category9 = Category(user_id=1, title="Hockey")

session.add(category9)
session.commit()

# Items

categoryItem1 = CategoryItem(user_id=1, title="Stick", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=9)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, title="Goggles", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=5)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, title="Snowboard", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=5)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, title="Two Shinguards", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=1)
session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1, title="Shinguards", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=1)
session.add(categoryItem5)
session.commit()

categoryItem6 = CategoryItem(user_id=1, title="Frisbee", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=4)
session.add(categoryItem6)
session.commit()

categoryItem7 = CategoryItem(user_id=1, title="Bat", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=3)
session.add(categoryItem7)
session.commit()

categoryItem8 = CategoryItem(user_id=1, title="Jersey", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=1)
session.add(categoryItem8)
session.commit()

categoryItem9 = CategoryItem(user_id=1, title="Soccer Cleats", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna a deserunt mollit anim id est laborum.", category_id=1)
session.add(categoryItem9)
session.commit()

print "added some categories and items!"
