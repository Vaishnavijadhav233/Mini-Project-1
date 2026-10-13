from flask import Flask, request, redirect, render_template_string
import sqlite3, datetime
app = Flask(__name__)
DB = "/data/library.db"

def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

with db() as c:
    c.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, due TEXT)")
    if c.execute("SELECT COUNT(*) FROM books").fetchone()[0] == 0:
        c.executemany("INSERT INTO books(title,author) VALUES(?,?)", [
            ("Operating System Concepts","Silberschatz"), ("Clean Code","Robert Martin"),
            ("Database System Concepts","Korth"), ("The Phoenix Project","Gene Kim")])

PAGE = """<h2>Library Management Platform</h2>
<form><input name=q placeholder="Search title"><button>Search</button></form>
<p><b>{{msg}}</b></p>
<table border=1 cellpadding=6><tr><th>ID</th><th>Title</th><th>Author</th><th>Status</th><th>Action</th></tr>
{% for b in books %}<tr><td>{{b.id}}</td><td>{{b.title}}</td><td>{{b.author}}</td>
<td>{{'Issued, due '+b.due if b.due else 'Available'}}</td>
<td>{% if b.due %}<a href="/return/{{b.id}}">Return</a>{% else %}<a href="/issue/{{b.id}}">Issue</a>{% endif %}</td></tr>{% endfor %}</table>"""

@app.route("/")
def home():
    q = request.args.get("q", "")
    rows = db().execute("SELECT * FROM books WHERE title LIKE ?", (f"%{q}%",)).fetchall()
    return render_template_string(PAGE, books=rows, msg=request.args.get("msg", ""))

@app.route("/issue/<int:i>")
def issue(i):
    due = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
    with db() as c: c.execute("UPDATE books SET due=? WHERE id=? AND due IS NULL", (due, i))
    return redirect("/")

@app.route("/return/<int:i>")
def ret(i):
    c = db(); r = c.execute("SELECT due FROM books WHERE id=?", (i,)).fetchone()
    late = max(0, (datetime.date.today() - datetime.date.fromisoformat(r["due"])).days) if r and r["due"] else 0
    with c: c.execute("UPDATE books SET due=NULL WHERE id=?", (i,))
    return redirect(f"/?msg=Book returned. Fine: Rs {late*5}")