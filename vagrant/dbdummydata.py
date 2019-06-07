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
User1 = User(name="dummy user", email="m.da7th@gmail.com",
             picture='')
session.add(User1)
session.commit()

# Category 1
category1 = Category(user_id=1, title="category 1")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=1)

session.add(categoryItem1)
session.commit()

categoryItem3 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=1)

session.add(categoryItem1)
session.commit()

categoryItem4 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=1)

session.add(categoryItem1)
session.commit()

categoryItem5 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=1)

session.add(categoryItem1)
session.commit()


# Category 2
category2 = Category(user_id=1, title="category 2")

session.add(category2)
session.commit()

categoryItem1 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=2)

session.add(categoryItem1)
session.commit()

categoryItem3 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=2)

session.add(categoryItem1)
session.commit()

categoryItem4 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=2)

session.add(categoryItem1)
session.commit()

categoryItem5 = CategoryItem(user_id=1, title="item title", description="description here...", category_id=2)

session.add(categoryItem2)
session.commit()

print "added some categories and items!"
