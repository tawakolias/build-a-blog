from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:3306/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(225))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/movie', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)


@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')
def get_blog():

    return Blog.query.all()

@app.route('/', methods=['POST', 'GET'])
def blog_fun():
    
    return render_template('blog.html',blog_c=get_blog())


@app.route('/blog_new', methods=['POST', 'GET'])
def new_entry():
    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']
       
        if not title:
            error = "Enter title for your blog"
            return render_template('/new.html', error = error )
        elif not body:
            error = "Enter body for your blog"
            return render_template('/new.html', error = error )         
        blog = Blog(title=title, body=body)
        db.session.add(blog)
        db.session.commit()
        blogurl = "/blog?id="+ str(blog.id) 
        return redirect(blogurl)
    else:
        return render_template('new.html')
          



@app.route('/blog', methods=['GET'])
def trouble_one():
    
    blogid = request.args.get('id')
    abc = Blog.query.filter_by(id = blogid).first()
    return render_template('entry.html', abc=abc)

if __name__ == '__main__':
    app.run()