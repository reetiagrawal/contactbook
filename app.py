from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "flash message"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '!Admin123'
app.config['MYSQL_DB'] = 'contactbook'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contactinfo")
    info = cur.fetchall()
    cur.close()
    return render_template('home.html', contactinfo = info)


@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/edit1' , methods = ['POST','GET'])
def edit1():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contactinfo SET name=%s,email=%s,contact=%s
        WHERE id=%s 
        """ , (name,email,contact,id))
        mysql.connection.commit()
        return redirect(url_for('home'))


@app.route('/add1', methods = ['POST'])
def add1():
    if request.method == "POST":

        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contactinfo (name,email,contact) VALUES (%s,%s,%s)",(name,email,contact))
        mysql.connection.commit()
        flash("Successfully Added")
        return redirect(url_for('add'))

@app.route('/delete/<string:id>' , methods = ['POST','GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contactinfo WHERE id = %s",(id))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/result' , methods = ['POST','GET'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("select name,email,contact from contactinfo where name ='"+name+"' and email = '"+email+"'")
        r = cur.fetchone()
        cur.close()
        return render_template("searchingbyname.html",r=r)

def page():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = page.paginate(page = page, per_page = 10)
    return render_template('home.html',page=page)










if __name__ == "__main__":
    app.run(debug=True)