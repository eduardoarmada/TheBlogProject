from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Returns the index file in which is displayed the info for each one of the posts store in the data file"""
    with open("static/data.json", "r") as handler:
        blog_posts = json.loads(handler.read())

    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """If accessed the /add filepath, returns the add file in order to fill up a form, adn when sent,
     return teh index page with the new info"""
    if request.method == "POST":
        # Obtains the information from the form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Adds the new post to the data file
        with open("static/data.json", "r") as handler:
            blog_posts = json.loads(handler.read())
            if len([post['id'] for post in blog_posts]) == 0:
                new_post_id = 1
            else:
                new_post_id = max([post['id'] for post in blog_posts]) + 1
            blog_posts.append({'id': new_post_id, 'author': author, 'title': title, 'content': content})
        with open("static/data.json", "w") as handler:
            handler.write(json.dumps(blog_posts))

        return redirect(url_for("index"))
    else:
        return render_template("add.html")


@app.route("/delete/<int:id_number>", methods=["GET", "POST"])
def delete_post(id_number):
    """If accessed the /delete filepath, a html file is rendered from the delete.html template with the id number of the
    post to delete, and a submit button to confirm the action, and if the action is confirmed, the index file will be
    returned with the updated posts information"""
    if request.method == "POST":
        # Deletes the post with the specified id
        with open("static/data.json", "r") as handler:
            blog_posts = json.loads(handler.read())
            for post in blog_posts:
                if post['id'] == id_number:
                    del blog_posts[blog_posts.index(post)]
                    break
        with open("static/data.json", "w") as handler:
            handler.write(json.dumps(blog_posts))

        return redirect(url_for("index"))
    else:
        return render_template("delete.html", id_number=id_number)


@app.route("/update/<int:id_number>", methods=["GET", "POST"])
def update(id_number):
    """If accessed the /update filepath, a html file is rendered from the update.html template that contains a form
    to fill to update the title and content of the post to update, and when sent the form, render the index file with
    the updated information of the posts"""
    if request.method == "POST":
        # Get infor
        title = request.form.get('title')
        content = request.form.get('content')

        with open("static/data.json", "r") as handler:
            blog_posts = json.loads(handler.read())
            for post in blog_posts:
                if post['id'] == id_number:
                    post['title'] = title
                    post['content'] = content
                    break

        with open("static/data.json", "w") as handler:
            handler.write(json.dumps(blog_posts))

        return redirect(url_for("index"))
    else:
        return render_template("update.html", id_number=id_number)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
