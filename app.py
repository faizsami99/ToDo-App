from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)



class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return  "ToDo" + str(self.id)

class Blogger(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    Author = db.Column(db.String(15), nullable=False, default="N/A")
    Blog = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Blogger " + str(self.id)



@app.route("/", methods=['GET', 'POST'])
def Home():
    if request.method == "POST":
        post = request.form['title']
        if post:
            new_post = ToDo(work=post)
            db.session.add(new_post)
            db.session.commit()
            return redirect("/")
        else:
            return redirect("/error")
    else:
        all_list = ToDo.query.all()
        return render_template("Home.html", posts=all_list)

@app.route("/Home/delete/<int:id>")
def Delete(id):
    post = ToDo.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

@app.route("/Home/Edit/<int:id>", methods=['GET', 'POST'])
def Edit(id):
    post = ToDo.query.get(id)
    if request.method == "POST":
        post.work = request.form['title']
        db.session.commit()
        return redirect("/")
    else:
        return render_template("edit.html", posts=post)

@app.route("/error")
def Error404():
    return render_template("error.html")

@app.route("/blogs", methods=['GET', 'POST'])
def Blogs():
    if request.method == "POST":
        new_title = request.form['title']
        new_author = request.form['author']
        new_blog = request.form['blog']
        new_post = Blogger(title=new_title, Author=new_author, Blog=new_blog)
        db.session.add(new_post)
        db.session.commit() 
        return redirect("/blogs")
    else:
        all_blogs = Blogger.query.all()
        return render_template("blogs.html", all_blogs=all_blogs)

@app.route("/blogs/blogdelete/<int:id>", methods=['GET', 'POST'])
def BlogDelete(id):
    post = Blogger.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/blogs")

@app.route("/blogs/new_post", methods=['GET', 'POST'])
def NewPost():
    if request.method == "POST":
        new_title = request.form['title']
        new_author = request.form['author']
        new_blog = request.form['blog']
        new_post = Blogger(title=new_title, Author=new_author, Blog=new_blog)
        db.session.add(new_post)
        db.session.commit() 
        return redirect("/blogs")
    return render_template("new_blog.html")

@app.route("/blogs/blogedit/<int:id>", methods=['GET', 'POST'])
def BlogEdit(id):
    post = Blogger.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.Author = request.form['author']
        post.Blog = request.form['blog']
        db.session.commit()
        return redirect("/blogs")
    else:
        return render_template("blogedit.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
