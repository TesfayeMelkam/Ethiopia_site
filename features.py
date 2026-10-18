"""More features: map, weather, languages, learn, recipes, people, directory, stories, polls, kids,
compare, stats, open data, printable guides, leaderboard, moderation, import, analytics."""
import csv, io, re, sqlite3, json
from datetime import date, timedelta
from flask import render_template, request, redirect, url_for, session, flash, jsonify, abort, Response
from seed5 import *
from seed4 import KNOW

def setup_db(DB):
    c = sqlite3.connect(DB)
    rc = [r[1] for r in c.execute("PRAGMA table_info(regions)")]
    for col in ("lat", "lng"):
        if col not in rc: c.execute(f"ALTER TABLE regions ADD COLUMN {col} REAL")
    for slug, (la, ln) in COORDS.items(): c.execute("UPDATE regions SET lat=?,lng=? WHERE slug=? AND lat IS NULL", (la, ln, slug))
    c.executescript("""CREATE TABLE IF NOT EXISTS directory(id INTEGER PRIMARY KEY AUTOINCREMENT,region,category,name,description,address,phone,website,approved INTEGER DEFAULT 1,created DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS stories(id INTEGER PRIMARY KEY AUTOINCREMENT,name,title,body,region,approved INTEGER DEFAULT 0,created DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS subscribers(id INTEGER PRIMARY KEY AUTOINCREMENT,email UNIQUE,created DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS polls(id INTEGER PRIMARY KEY AUTOINCREMENT,question);
    CREATE TABLE IF NOT EXISTS poll_opts(id INTEGER PRIMARY KEY AUTOINCREMENT,poll_id INTEGER,text,votes INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY AUTOINCREMENT,name,score INTEGER,total INTEGER,created DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS visits(day TEXT PRIMARY KEY,n INTEGER);
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,action,created DEFAULT CURRENT_TIMESTAMP);""")
    for d in DIRECTORY:
        if not c.execute("SELECT 1 FROM directory WHERE name=?", (d[2],)).fetchone():
            c.execute("INSERT INTO directory(region,category,name,description,address) VALUES(?,?,?,?,?)", (d[0], d[1], d[2], d[3], d[4]))
    if not c.execute("SELECT 1 FROM polls").fetchone():
        pid = c.execute("INSERT INTO polls(question) VALUES(?)", (POLL[0],)).lastrowid
        c.executemany("INSERT INTO poll_opts(poll_id,text) VALUES(?,?)", [(pid, o) for o in POLL[1]])
    c.commit(); c.close()

def num(s):
    m = re.search(r"\d[\d,\.]*", s or "")
    try: return float(m.group().replace(",", "").rstrip(".")) if m else 0
    except ValueError: return 0

TABLES = {"regions": "SELECT slug,name,name_am,capital,population,area,languages,about FROM regions", "zones": "SELECT slug,region,name,center,about FROM zones",
          "items": "SELECT id,region,zone,kind,title,description FROM items", "events": "SELECT title,date_text,description,region,kind FROM events"}

def register(app, db, admin_required):
    @app.context_processor
    def ctx():
        lang = session.get("lang", "en"); tr = I18N.get(lang, I18N["en"])
        return {"t": lambda k: tr.get(k, I18N["en"].get(k, k)), "lang": lang, "csrf": lambda: session.get("t", "")}

    @app.route("/lang/<code>")
    def setlang(code):
        if code in I18N: session["lang"] = code
        return redirect(request.referrer or url_for("index"))

    @app.route("/map")
    def map_page():
        d = db(); pts = [{"name": r["name"], "lat": r["lat"], "lng": r["lng"], "kind": "region", "url": url_for("region", slug=r["slug"])} for r in d.execute("SELECT slug,name,lat,lng FROM regions WHERE lat IS NOT NULL")]
        pts += [{"name": n, "lat": la, "lng": ln, "kind": k, "url": url_for("search", q=n.split(" (")[0])} for n, la, ln, rg, k in MAPPTS]
        return render_template("map.html", pts=pts)

    @app.route("/learn")
    def learn():
        cards = [[a, f"{r} = {n}"] for a, r, n in NUMBERS] + [[a, f"{r} = {e}"] for a, r, e in DAYS] + [[a, f"{r} = {e}"] for a, r, e in KNOW["phrases"]]
        return render_template("learn.html", FIDEL=FIDEL, V=VOWELS, NUMBERS=NUMBERS, DAYS=DAYS, phrases=KNOW["phrases"], cards=cards)

    @app.route("/recipes")
    def recipes(): return render_template("recipes.html", R=RECIPES)

    @app.route("/people")
    def people(): return render_template("people.html", P=PEOPLE, D=DYNASTIES, cats=sorted({p[1] for p in PEOPLE}))

    @app.route("/kids")
    def kids(): return render_template("kids.html", K=KIDS)

    # ---- directory
    @app.route("/directory")
    def directory():
        rows = db().execute("SELECT d.*,r.name rname FROM directory d LEFT JOIN regions r ON r.slug=d.region WHERE approved=1 ORDER BY category,name").fetchall()
        return render_template("directory.html", rows=rows, cats=sorted({r["category"] for r in rows}))

    @app.route("/directory/submit", methods=["POST"])
    def directory_submit():
        f = request.form
        if not f.get("website_hp") and f.get("name", "").strip():
            db().execute("INSERT INTO directory(region,category,name,description,address,phone,website,approved) VALUES(?,?,?,?,?,?,?,0)", (f.get("region") or None, f.get("category", "other")[:30], f["name"][:100], f.get("description", "")[:600], f.get("address", "")[:150], f.get("phone", "")[:40], f.get("website", "")[:200])); db().commit()
            flash("Thank you! Your listing will appear after review.")
        return redirect(url_for("directory"))

    # ---- stories / polls / newsletter
    @app.route("/stories")
    def stories():
        return render_template("stories.html", rows=db().execute("SELECT s.*,r.name rname FROM stories s LEFT JOIN regions r ON r.slug=s.region WHERE approved=1 ORDER BY id DESC").fetchall())

    @app.route("/stories/submit", methods=["POST"])
    def stories_submit():
        f = request.form
        if not f.get("website") and f.get("body", "").strip() and f.get("title", "").strip():
            db().execute("INSERT INTO stories(name,title,body,region) VALUES(?,?,?,?)", ((f.get("name") or "Visitor")[:40], f["title"][:100], f["body"][:3000], f.get("region") or None)); db().commit()
            flash("Thank you! Your story will appear after review.")
        return redirect(url_for("stories"))

    @app.route("/polls")
    def polls():
        d = db(); p = d.execute("SELECT * FROM polls ORDER BY id DESC LIMIT 1").fetchone()
        opts = d.execute("SELECT * FROM poll_opts WHERE poll_id=?", (p["id"],)).fetchall()
        return render_template("polls.html", p=p, opts=opts, total=sum(o["votes"] for o in opts) or 1, voted=session.get(f"v{p['id']}"))

    @app.route("/polls/vote", methods=["POST"])
    def poll_vote():
        o = request.form.get("opt", "")
        row = db().execute("SELECT poll_id FROM poll_opts WHERE id=?", (o,)).fetchone() if o.isdigit() else None
        if row and not session.get(f"v{row['poll_id']}"):
            db().execute("UPDATE poll_opts SET votes=votes+1 WHERE id=?", (o,)); db().commit(); session[f"v{row['poll_id']}"] = 1
        return redirect(url_for("polls"))

    @app.route("/subscribe", methods=["POST"])
    def subscribe():
        e = request.form.get("email", "").strip()[:120]
        if not request.form.get("website") and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e):
            db().execute("INSERT OR IGNORE INTO subscribers(email) VALUES(?)", (e,)); db().commit(); flash("Subscribed. Thank you!")
        return redirect(request.referrer or url_for("index"))

    @app.route("/quiz/score", methods=["POST"])
    def quiz_score():
        f = request.form
        try: s, n = int(f["score"]), int(f["total"])
        except (KeyError, ValueError): abort(400)
        if 0 <= s <= n <= 20 and not session.get("scored"):
            db().execute("INSERT INTO scores(name,score,total) VALUES(?,?,?)", ((f.get("name") or "Anonymous")[:30], s, n)); db().commit(); session["scored"] = 1
        return jsonify(ok=True)

    # ---- compare / stats / data / printables
    @app.route("/compare")
    def compare():
        d = db(); a, b = request.args.get("a"), request.args.get("b"); cols = []
        for s in (a, b):
            r = d.execute("SELECT * FROM regions WHERE slug=?", (s,)).fetchone() if s else None
            if r: cols.append((r, d.execute("SELECT COUNT(*) FROM zones WHERE region=?", (s,)).fetchone()[0], d.execute("SELECT COUNT(*) FROM items WHERE region=?", (s,)).fetchone()[0]))
        return render_template("compare.html", cols=cols, a=a, b=b)

    @app.route("/stats")
    def stats():
        regs = db().execute("SELECT name,slug,population,area FROM regions").fetchall()
        pop = sorted([(r["name"], num(r["population"])) for r in regs], key=lambda x: -x[1]); area = sorted([(r["name"], num(r["area"])) for r in regs], key=lambda x: -x[1])
        counts = db().execute("SELECT kind,COUNT(*) n FROM items GROUP BY kind ORDER BY n DESC").fetchall()
        return render_template("stats.html", pop=pop, area=area, counts=counts, total=round(sum(p[1] for p in pop), 1))

    @app.route("/data")
    def data(): return render_template("data.html", names=list(TABLES))

    @app.route("/data/<name>.<ext>")
    def data_file(name, ext):
        if name not in TABLES or ext not in ("csv", "json"): abort(404)
        rows = [dict(r) for r in db().execute(TABLES[name])]
        if ext == "json": return jsonify(rows)
        out = io.StringIO(); w = csv.DictWriter(out, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        return Response("\ufeff" + out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={name}.csv"})

    @app.route("/downloads")
    def downloads():
        return render_template("downloads.html", regs=db().execute("SELECT slug,name FROM regions ORDER BY name").fetchall())

    @app.route("/guide/<slug>")
    def guide(slug):
        d = db(); r = d.execute("SELECT * FROM regions WHERE slug=?", (slug,)).fetchone() or abort(404)
        return render_template("guide.html", r=r, zones=d.execute("SELECT * FROM zones WHERE region=?", (slug,)).fetchall(), items=d.execute("SELECT * FROM items WHERE region=? AND kind IN ('city','church','tourism','culture')", (slug,)).fetchall(), fests=d.execute("SELECT * FROM events WHERE region=?", (slug,)).fetchall())

    @app.route("/worksheet/<slug>")
    def worksheet(slug):
        d = db(); r = d.execute("SELECT * FROM regions WHERE slug=?", (slug,)).fetchone() or abort(404)
        return render_template("worksheet.html", r=r, zones=d.execute("SELECT name FROM zones WHERE region=?", (slug,)).fetchall(), cities=d.execute("SELECT title FROM items WHERE region=? AND kind='city' LIMIT 6", (slug,)).fetchall(), places=d.execute("SELECT title FROM items WHERE region=? AND kind IN ('tourism','church') LIMIT 6", (slug,)).fetchall())

    # ---- admin: moderation, import, subscribers
    @app.route("/admin/more", methods=["GET", "POST"])
    @admin_required
    def admin_more():
        d = db(); f = request.form
        if request.method == "POST":
            act, i = f.get("action"), f.get("id", "")
            sql = {"dir_ok": "UPDATE directory SET approved=1 WHERE id=?", "dir_del": "DELETE FROM directory WHERE id=?", "story_ok": "UPDATE stories SET approved=1 WHERE id=?", "story_del": "DELETE FROM stories WHERE id=?", "sub_del": "DELETE FROM subscribers WHERE id=?"}
            if act in sql and i.isdigit(): d.execute(sql[act], (i,)); flash("Done")
            elif act == "dir_add" and f.get("name"):
                d.execute("INSERT INTO directory(region,category,name,description,address,phone,website,approved) VALUES(?,?,?,?,?,?,?,1)", (f.get("region") or None, f.get("category", "other"), f["name"], f.get("description"), f.get("address"), f.get("phone"), f.get("website"))); flash("Listing added")
            elif act == "import":
                up = request.files.get("csv"); n = 0
                if up and up.filename:
                    valid = {r[0] for r in d.execute("SELECT slug FROM regions")}
                    for row in csv.DictReader(io.StringIO(up.read().decode("utf-8-sig"))):
                        if row.get("region") in valid and row.get("title"):
                            d.execute("INSERT INTO items(region,zone,kind,title,description,link) VALUES(?,?,?,?,?,?)", (row["region"], row.get("zone") or None, row.get("kind") or "city", row["title"], row.get("description"), row.get("link"))); n += 1
                flash(f"Imported {n} rows")
            d.commit(); return redirect(url_for("admin_more"))
        q = lambda s: d.execute(s).fetchall()
        days = [(date.today() - timedelta(days=k)).isoformat() for k in range(6, -1, -1)]
        vis = {r["day"]: r["n"] for r in q("SELECT * FROM visits")}
        return render_template("admin_more.html", dirs=q("SELECT * FROM directory ORDER BY approved,id DESC"), stories=q("SELECT * FROM stories ORDER BY approved,id DESC"), subs=q("SELECT * FROM subscribers ORDER BY id DESC"), audit=q("SELECT * FROM audit ORDER BY id DESC LIMIT 40"), visits=[(x[5:], vis.get(x, 0)) for x in days], scores=q("SELECT * FROM scores ORDER BY id DESC LIMIT 10"))

    @app.route("/admin/subscribers.csv")
    @admin_required
    def subs_csv():
        return Response("email,created\n" + "\n".join(f"{r['email']},{r['created']}" for r in db().execute("SELECT * FROM subscribers")), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=subscribers.csv"})

    @app.after_request
    def track(resp):
        try:
            if request.method == "GET" and resp.status_code == 200 and resp.mimetype == "text/html" and not request.path.startswith(("/admin", "/static")):
                db().execute("INSERT INTO visits(day,n) VALUES(?,1) ON CONFLICT(day) DO UPDATE SET n=n+1", (date.today().isoformat(),)); db().commit()
            elif request.method == "POST" and session.get("admin") and request.path.startswith("/admin"):
                db().execute("INSERT INTO audit(action) VALUES(?)", (f"{request.method} {request.path}",)); db().commit()
        except Exception: pass
        return resp
