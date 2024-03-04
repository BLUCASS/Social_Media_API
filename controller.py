from model import engine, User, Posts
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()


class DbManagement:
    
    """This class will manage the user's database"""
    
    def insert_user(self, data) -> None:
        """It will insert an user with its information in the database"""
        user = User(email=data["email"].lower(),
                    name=data["name"].title().strip(),
                    password=self.cryptograph_password(data["password"]))
        try:
            session.add(user)
        except:
            session.rollback()
        else:
            session.commit()
            session.close()


    def verify_data(self, data) -> bool:
        """It receives the inserted email and password and checks if the user exists.
        If true, returns the user's ID"""
        encrypted_password = self.cryptograph_password(data["password"])
        try:
            user = session.query(User).filter(User.email == data["email"]).first()
            if user.password == encrypted_password:
                return user.id
            raise IndexError
        except:
            return False
        
    def cryptograph_password(self, password) -> str:
        """It receives a password and returns it as a sha256 hash"""
        from hashlib import sha256
        encrypted_password = sha256(password.encode()).hexdigest()
        return encrypted_password
    
    def return_user(self, id) -> str:
        """It receives an ID, search in the database and returns the user's data"""
        user = session.query(User).filter(User.id==id).first()
        return user
    

class PostsManagement:
    
    """This class will manage the posts database"""
    
    def insert_post(self, message, id) -> bool:
        """It receives a post as a message and an User ID and isert it in the database"""
        posts = Posts(owner_id=id,
                      post=message.capitalize()[0:86])
        try:
            session.add(posts)
        except:
            session.rollback()
            session.close()
            return False
        else:
            session.commit()
            session.close()
            return True
        
    def get_posts(self, id) -> str:
        """It receives an User ID and returns its posts"""
        try:
            posts = session.query(Posts).filter(Posts.owner_id==id).all()
            return posts
        except:
            return False
        
    def delete_post(self, id) -> None:
        """It receives a post ID and deletes it"""
        try:
            post = session.query(Posts).filter(Posts.id == id).first()
            session.delete(post)
        except:
            session.rollback()
        else:
            session.commit()