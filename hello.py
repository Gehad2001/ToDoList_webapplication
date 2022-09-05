from urllib import request
from flask import Flask,request,redirect
from flask import url_for,flash
from flask import render_template
from werkzeug.utils import secure_filename
from database import get_db
import os

UPLOAD_FOLDER ="static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key ="secret key"

@app.route("/")
@app.route('/<firstname>/<lastname>')
def index_page(firstname="" , lastname=""):
       conn = get_db().cursor()
       conn.execute("select * from todo;")
       data = conn.fetchall()
       print(data)
       return render_template("index.html", firstname=firstname , lastname=lastname , data=data)



@app.route("/add", methods=['POST','GET'])
def add():
      if request.method == "POST":
             txt = request.form['txt']
             conn = get_db()
             conn.execute(f"INSERT INTO todo (txt) values('{txt}');")
             conn.commit()
             conn.close()
             return redirect(url_for('index_page',txt=txt ))
      return render_template("add.html")
   
     
   
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
       conn=get_db()
       if request.method=="POST":
              txt = request.form['txt']
              conn.execute(f"update todo set txt='{txt}' where id={id}")
              conn.commit()
              conn.close()
       elif request.method=="GET":
              conn = conn.cursor().execute(f"select * from todo where id ={id}")
              row = conn.fetchone()
              conn.close()
              return render_template("update.html",row=row)
       return redirect(url_for("index_page"))      

@app.route("/delete/<int:id>")
def delete(id):
       conn=get_db()
       conn.execute(f"delete from todo where id={id} ")
       conn.commit()
       conn.close()
       return redirect(url_for("index_page"))  

@app.post("/search")
def search( ):
       if 'txt' in request.form:
        txt=request.form['txt']
        conn=get_db().cursor()
        conn.execute(f"select * from todo  WHERE txt  like '{txt}%'")
        data=conn.fetchall()
        conn.close()
        return render_template("search.html",data=data)

@app.route("/done/<int:id>")
def status_done(id):
       conn=get_db()
       conn.execute(f"update todo set  task_status=true where id={id}")
       conn.commit()
       conn.close()
       return redirect(url_for("index_page"))  


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route("/upload_form", methods=["GET","POST"])
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

  
