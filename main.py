from flask import Flask, render_template, request, redirect, url_for
from controller import DbManagement, PostsManagement


# CREATING THE APP
app = Flask(__name__)


# SETTING THE INDEX PAGE
@app.route('/', methods=['GET'])
def index():
    """It returns the index page"""
    return render_template('index.html')


# CREATING THE SIGN IN ROUTE
@app.route('/sign_in')
def sign_in():
    """It returns the sign in page"""
    return render_template('sign_in.html')

# THIS ROUTE ONLY VERIFIES THE USER'S INFORMATION TO SIGN IN
@app.route('/verify', methods=['POST'])
def verify():
    """If the credentials exist, it returns the user's page. Else, returns the
    user to the sign in page."""
    data = request.form
    user = DbManagement().verify_data(data)
    if user: return redirect(url_for('user', id=user))
    return redirect(url_for('sign_in'))
    
# THIS ROUTE DEFINES THE USER'S PAGE
@app.route('/user/<int:id>')
def user(id):
    """Returns the user's homepage"""
    user = DbManagement().return_user(id)
    return render_template("user_page.html", user=user)

# THIS ROUTE SHOWS THE USER'S POSTS
@app.route('/user/<int:id>/posts')
def posts(id):
    """It returns a page showing all the user's posts from the database"""
    posts = PostsManagement().get_posts(id)
    user = DbManagement().return_user(id)
    return render_template("posts.html", user=user, posts=posts)

# THIS ROUTE ENTERS A NEW POST
@app.route('/send/post', methods=['POST'])
def send_post():
    """It sends a posts to the class Posts Management, which will insert it in
    the database with the user's ID as owner_id"""
    data = request.form
    PostsManagement().insert_post(data["message"], data["id"])
    return redirect(url_for("posts", id=data["id"]))

# THIS ROUTE DELETES A POST SENDING THE ID
@app.route('/delete/<int:id_user>/<int:id_post>', methods=['GET'])
def delete(id_user, id_post):
    """It deletes a post sending the User ID and the Post ID"""
    PostsManagement().delete_post(id_post)
    return redirect(url_for('posts', id=id_user))



# CREATING THE SIGN UP ROUTE
@app.route('/sign_up', methods=['GET'])
def sign_up():
    """It returns the sign up page"""
    return render_template('sign_up.html')


# THIS ROUTE ONLY SENDS THE USER'S DATA
@app.route('/send_data', methods=['POST'])
def send_data():
    """It sends the user's name, email and password. The class DB Management
    will receive it and insert the user in the database"""
    data = request.form
    DbManagement().insert_user(data)
    return redirect(url_for('index'))




# RUNNING THE APP
if __name__ == '__main__':
    app.run(debug=True)



