"""Extra back-end: dashboard, comments, contact, events, API, editing."""
import os, uuid, sqlite3, json
from flask import render_template, request, redirect, url_for, session, flash, jsonify, abort, Response
from werkzeug.utils import secure_filename
from seed2 import EXTRA, EVENTS, FACTS
from seed3 import Z, I, TRAVEL
from seed4 import BOOKS, KNOW, QUIZ, FESTIVALS, AM

slugify = lambda n: n.lower().replace(" ", "-").replace("(", "").replace(")", "")

def setup_db(DB):
    c = sqlite3.connect(DB)
    rc = [r[1] for r in c.execute("PRAGMA table_info(regions)")]
    for col in ["history", "culture", "tourism", "economy", "food", "climate", "cover", "travel"]:
        if col not in rc: c.execute(f"ALTER TABLE regions ADD COLUMN {col} TEXT")
    if "views" not in rc: c.execute("ALTER TABLE regions ADD COLUMN views INTEGER DEFAULT 0")
    if "views" not in [r[1] for r in c.execute("PRAGMA table_info(zones)")]:
        c.execute("ALTER TABLE zones ADD COLUMN views INTEGER DEFAULT 0")
    c.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,name,email,body,created DEFAULT CURRENT_TIMESTAMP)")
    c.execute("CREATE TABLE IF NOT EXISTS comments(id INTEGER PRIMARY KEY AUTOINCREMENT,kind,slug,name,body,rating INTEGER,created DEFAULT CURRENT_TIMESTAMP)")
    c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,title,date_text,description,sort INTEGER DEFAULT 0)")
    for slug, v in EXTRA.items():
        c.execute("UPDATE regions SET history=?,culture=?,tourism=?,economy=?,food=?,climate=? WHERE slug=? AND history IS NULL", (*v, slug))
    for slug, t in TRAVEL.items():
        c.execute("UPDATE regions SET travel=? WHERE slug=? AND travel IS NULL", (t, slug))
    for reg, name, center, about, hist, cult, tour, eco in Z:
        zs = slugify(name)
        if not c.execute("SELECT 1 FROM zones WHERE slug=?", (zs,)).fetchone():
            c.execute("INSERT INTO zones(slug,region,name,center,about,history,culture,tourism,economy) VALUES(?,?,?,?,?,?,?,?,?)", (zs, reg, name, center, about, hist, cult, tour, eco))
            c.execute("INSERT INTO items(region,zone,kind,title,description) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM items WHERE region=? AND title=?)", (reg, zs, "city", center, f"Main town of {name}.", reg, center))
    for reg, zn, kind, title, desc in I:
        c.execute("INSERT INTO items(region,zone,kind,title,description) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM items WHERE region=? AND title=?)", (reg, slugify(zn) if zn else None, kind, title, desc, reg, title))
    if c.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
        c.executemany("INSERT INTO events(title,date_text,description,sort) VALUES(?,?,?,?)", [(*e, i) for i, e in enumerate(EVENTS)])
    ec = [r[1] for r in c.execute("PRAGMA table_info(events)")]
    for col in ["region", "kind"]:
        if col not in ec: c.execute(f"ALTER TABLE events ADD COLUMN {col} TEXT")
    c.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT,title,author,category,region,description,file,cover,content,views INTEGER DEFAULT 0,created DEFAULT CURRENT_TIMESTAMP)")
    for i, (t, dt, ds, rg, kd) in enumerate(FESTIVALS):
        row = c.execute("SELECT id FROM events WHERE title=?", (t,)).fetchone()
        if row: c.execute("UPDATE events SET region=COALESCE(region,?),kind=COALESCE(kind,?) WHERE id=?", (rg, kd, row[0]))
        else: c.execute("INSERT INTO events(title,date_text,description,sort,region,kind) VALUES(?,?,?,?,?,?)", (t, dt, ds, 100 + i, rg, kd))
    if "name_am" not in [r[1] for r in c.execute("PRAGMA table_info(regions)")]:
        c.execute("ALTER TABLE regions ADD COLUMN name_am TEXT")
    for slug, am in AM.items(): c.execute("UPDATE regions SET name_am=? WHERE slug=? AND name_am IS NULL", (am, slug))
    for b in BOOKS:
        if not c.execute("SELECT 1 FROM books WHERE title=?", (b[0],)).fetchone():
            c.execute("INSERT INTO books(title,author,category,region,description,content) VALUES(?,?,?,?,?,?)", b)
    c.commit(); c.close()

def register(app, db, admin_required, UPLOADS, ALLOWED):
    def save(f):
        if f and f.filename:
            if f.filename.rsplit(".", 1)[-1].lower() not in ALLOWED: return False
            fn = uuid.uuid4().hex[:8] + "_" + secure_filename(f.filename)
            p = os.path.join(UPLOADS, fn); f.save(p)
            if fn.rsplit(".", 1)[-1].lower() in ("jpg", "jpeg", "png", "webp"):
                try:
                    from PIL import Image
                    im = Image.open(p); im.thumbnail((1600, 1600)); im.save(p)
                except Exception: pass
            return fn
        return None

    @app.route("/")
    def index():
        d = db()
        regs = d.execute("SELECT * FROM regions").fetchall()
        counts = {r["kind"]: r["n"] for r in d.execute("SELECT kind,COUNT(*) n FROM items GROUP BY kind")}
        feat = d.execute("SELECT i.*,r.name rname FROM items i JOIN regions r ON r.slug=i.region WHERE kind IN ('tourism','church') ORDER BY RANDOM() LIMIT 8").fetchall()
        events = d.execute("SELECT * FROM events ORDER BY sort").fetchall()
        return render_template("index.html", regs=regs, counts=counts, feat=feat, events=events, facts=FACTS)

    @app.route("/region/<slug>")
    def region(slug):
        d = db()
        r = d.execute("SELECT * FROM regions WHERE slug=?", (slug,)).fetchone() or abort(404)
        d.execute("UPDATE regions SET views=COALESCE(views,0)+1 WHERE slug=?", (slug,)); d.commit()
        items = d.execute("SELECT * FROM items WHERE region=? ORDER BY id DESC", (slug,)).fetchall()
        zones = d.execute("SELECT * FROM zones WHERE region=? ORDER BY name", (slug,)).fetchall()
        comments = d.execute("SELECT * FROM comments WHERE kind='region' AND slug=? ORDER BY id DESC", (slug,)).fetchall()
        fests = d.execute("SELECT * FROM events WHERE region=? ORDER BY sort", (slug,)).fetchall()
        return render_template("region.html", r=r, items=items, zones=zones, comments=comments, fests=fests)

    @app.route("/zone/<slug>")
    def zone(slug):
        d = db()
        z = d.execute("SELECT * FROM zones WHERE slug=?", (slug,)).fetchone() or abort(404)
        d.execute("UPDATE zones SET views=COALESCE(views,0)+1 WHERE slug=?", (slug,)); d.commit()
        r = d.execute("SELECT * FROM regions WHERE slug=?", (z["region"],)).fetchone()
        items = d.execute("SELECT * FROM items WHERE zone=? ORDER BY id DESC", (slug,)).fetchall()
        comments = d.execute("SELECT * FROM comments WHERE kind='zone' AND slug=? ORDER BY id DESC", (slug,)).fetchall()
        sibs = d.execute("SELECT slug,name FROM zones WHERE region=? AND slug!=? ORDER BY name", (z["region"], slug)).fetchall()
        return render_template("zone.html", z=z, r=r, items=items, comments=comments, sibs=sibs)

    @app.route("/comment", methods=["POST"])
    def comment():
        f = request.form; body = f.get("body", "").strip()[:600]
        if f.get("website") or f.get("kind") not in ("region", "zone"): abort(400)  # honeypot / validation
        n = session.get("cn", 0)
        if body and n < 10:
            rating = min(5, max(1, int(f.get("rating", 5) or 5)))
            db().execute("INSERT INTO comments(kind,slug,name,body,rating) VALUES(?,?,?,?,?)", (f["kind"], f["slug"], (f.get("name") or "Visitor").strip()[:40], body, rating))
            db().commit(); session["cn"] = n + 1; flash("Thank you for your comment!")
        return redirect(request.referrer or url_for("index"))

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST" and not request.form.get("website") and request.form.get("body", "").strip():
            f = request.form
            db().execute("INSERT INTO messages(name,email,body) VALUES(?,?,?)", (f.get("name", "")[:60], f.get("email", "")[:80], f["body"][:2000])); db().commit()
            flash("Message sent. Thank you!"); return redirect(url_for("contact"))
        return render_template("contact.html")

    @app.route("/events")
    def events():
        return render_template("events.html", events=db().execute("SELECT e.*,r.name rname FROM events e LEFT JOIN regions r ON r.slug=e.region ORDER BY e.sort").fetchall())

    @app.route("/library")
    def library():
        d = db()
        books = d.execute("SELECT b.*,r.name rname FROM books b LEFT JOIN regions r ON r.slug=b.region ORDER BY b.id DESC").fetchall()
        legacy = d.execute("SELECT i.*,r.name rname FROM items i JOIN regions r ON r.slug=i.region WHERE kind='book' ORDER BY i.id DESC").fetchall()
        return render_template("library.html", books=books, legacy=legacy)

    @app.route("/library/<int:i>")
    def book(i):
        d = db(); b = d.execute("SELECT * FROM books WHERE id=?", (i,)).fetchone() or abort(404)
        d.execute("UPDATE books SET views=COALESCE(views,0)+1 WHERE id=?", (i,)); d.commit()
        return render_template("book.html", b=b)

    @app.route("/api/search")
    def api_search():
        q = request.args.get("q", "").strip(); out = []
        if len(q) >= 2:
            like = f"%{q}%"; d = db()
            for r in d.execute("SELECT slug,name FROM regions WHERE name LIKE ? OR name_am LIKE ? OR capital LIKE ? LIMIT 5", (like, like, like)): out.append({"t": r["name"], "k": "Region", "u": url_for("region", slug=r["slug"])})
            for z in d.execute("SELECT slug,name FROM zones WHERE name LIKE ? OR center LIKE ? LIMIT 5", (like, like)): out.append({"t": z["name"], "k": "Zone", "u": url_for("zone", slug=z["slug"])})
            for i in d.execute("SELECT title,kind,region,zone FROM items WHERE title LIKE ? LIMIT 8", (like,)): out.append({"t": i["title"], "k": i["kind"], "u": url_for("zone", slug=i["zone"]) if i["zone"] else url_for("region", slug=i["region"])})
            for b in d.execute("SELECT id,title FROM books WHERE title LIKE ? LIMIT 4", (like,)): out.append({"t": b["title"], "k": "Book", "u": url_for("book", i=b["id"])})
            for ev in d.execute("SELECT title FROM events WHERE title LIKE ? LIMIT 4", (like,)): out.append({"t": ev["title"], "k": "Festival", "u": url_for("events")})
        return jsonify(out)

    @app.route("/api/items")
    def api_items():
        ids = [int(x) for x in request.args.get("ids", "").split(",") if x.isdigit()][:100]
        if not ids: return jsonify([])
        rows = db().execute(f"SELECT i.id,i.title,i.description,i.kind,i.region,i.zone,r.name rname FROM items i JOIN regions r ON r.slug=i.region WHERE i.id IN ({','.join('?' * len(ids))})", ids).fetchall()
        return jsonify([{**dict(r), "url": url_for("zone", slug=r["zone"]) if r["zone"] else url_for("region", slug=r["region"])} for r in rows])

    @app.route("/favorites")
    def favorites():
        return render_template("favorites.html")

    @app.route("/planner")
    def planner():
        d = db(); sel = request.args.getlist("r")
        try: days = min(14, max(1, int(request.args.get("days", 3))))
        except ValueError: days = 3
        plan, tips = None, []
        if sel:
            per = max(1, days // len(sel)); flat = []
            for s in sel:
                flat += d.execute("SELECT i.*,r.name rname FROM items i JOIN regions r ON r.slug=i.region WHERE i.region=? AND kind IN ('tourism','church','culture','city') ORDER BY CASE kind WHEN 'tourism' THEN 0 WHEN 'church' THEN 1 WHEN 'culture' THEN 2 ELSE 3 END, i.id LIMIT ?", (s, per * 3)).fetchall()
                tips += d.execute("SELECT name,travel FROM regions WHERE slug=?", (s,)).fetchall()
            plan = [flat[i * 3:(i + 1) * 3] for i in range(days) if flat[i * 3:(i + 1) * 3]]
        return render_template("planner.html", plan=plan, sel=sel, days=days, tips=tips)

    @app.route("/sw.js")
    def sw(): return app.send_static_file("sw.js")

    @app.route("/robots.txt")
    def robots(): return Response(f"User-agent: *\nDisallow: /admin\nSitemap: {request.url_root}sitemap.xml\n", mimetype="text/plain")

    @app.route("/sitemap.xml")
    def sitemap():
        d = db(); base = request.url_root.rstrip("/")
        urls = ["/", "/regions", "/library", "/know", "/events", "/quiz", "/planner", "/about", "/contact"]
        urls += ["/region/" + r[0] for r in d.execute("SELECT slug FROM regions")] + ["/zone/" + r[0] for r in d.execute("SELECT slug FROM zones")] + ["/library/%d" % r[0] for r in d.execute("SELECT id FROM books")]
        return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{base}{u}</loc></url>" for u in urls) + "</urlset>", mimetype="application/xml")

    @app.route("/admin/export")
    @admin_required
    def export():
        data = {t: [dict(r) for r in db().execute(f"SELECT * FROM {t}")] for t in ["regions", "zones", "items", "books", "events", "comments", "messages"]}
        return Response(json.dumps(data, ensure_ascii=False, indent=1), mimetype="application/json", headers={"Content-Disposition": "attachment; filename=ethiopia_backup.json"})

    @app.route("/know")
    def know():
        return render_template("know.html", K=KNOW)

    @app.route("/quiz")
    def quiz():
        return render_template("quiz.html", Q=QUIZ, top=db().execute("SELECT name,score,total FROM scores ORDER BY score DESC,id DESC LIMIT 10").fetchall())

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/api/regions")
    def api_regions():
        return jsonify([dict(r) for r in db().execute("SELECT slug,name,capital,population,area,languages,about FROM regions")])

    @app.route("/api/region/<slug>")
    def api_region(slug):
        d = db(); r = d.execute("SELECT * FROM regions WHERE slug=?", (slug,)).fetchone() or abort(404)
        return jsonify(region=dict(r), zones=[dict(z) for z in d.execute("SELECT * FROM zones WHERE region=?", (slug,))], items=[dict(i) for i in d.execute("SELECT * FROM items WHERE region=?", (slug,))])

    # ---------- admin ----------
    @app.route("/admin", methods=["GET", "POST"])
    @admin_required
    def admin():
        d = db(); f = request.form
        if request.method == "POST":
            act = f.get("action", "item")
            if act == "zone":
                slug = secure_filename(f["name"].lower().replace(" ", "-"))
                d.execute("INSERT OR REPLACE INTO zones(slug,region,name,center,about,history,culture,tourism,economy) VALUES(?,?,?,?,?,?,?,?,?)", (slug, f["region"], f["name"], f.get("center"), f.get("about"), f.get("history"), f.get("culture"), f.get("tourism"), f.get("economy")))
            elif act == "event":
                d.execute("INSERT INTO events(title,date_text,description,sort,region,kind) VALUES(?,?,?,99,?,?)", (f["title"], f.get("date_text"), f.get("description"), f.get("region") or None, f.get("kind") or "cultural"))
            elif act == "book":
                fn = save(request.files.get("file")); cv = save(request.files.get("cover"))
                if fn is False or cv is False: flash("File type not allowed"); return redirect(url_for("admin"))
                d.execute("INSERT INTO books(title,author,category,region,description,file,cover,content) VALUES(?,?,?,?,?,?,?,?)", (f["title"], f.get("author"), f.get("category"), f.get("region") or None, f.get("description"), fn, cv, f.get("content") or None))
            else:
                fn = save(request.files.get("file"))
                if fn is False: flash("File type not allowed"); return redirect(url_for("admin"))
                d.execute("INSERT INTO items(region,kind,title,description,file,link,zone) VALUES(?,?,?,?,?,?,?)", (f["region"], f["kind"], f["title"], f["description"], fn, f.get("link"), f.get("zone") or None))
            d.commit(); flash("Saved"); return redirect(url_for("admin"))
        q = lambda s: d.execute(s).fetchall()
        stats = dict(items=q("SELECT COUNT(*) n FROM items")[0]["n"], zones=q("SELECT COUNT(*) n FROM zones")[0]["n"], comments=q("SELECT COUNT(*) n FROM comments")[0]["n"], messages=q("SELECT COUNT(*) n FROM messages")[0]["n"], views=q("SELECT COALESCE(SUM(views),0) n FROM regions")[0]["n"])
        return render_template("admin.html", stats=stats,
            items=q("SELECT i.*,r.name rname FROM items i JOIN regions r ON r.slug=i.region ORDER BY i.id DESC"),
            messages=q("SELECT * FROM messages ORDER BY id DESC"), comments=q("SELECT * FROM comments ORDER BY id DESC"),
            events=q("SELECT * FROM events ORDER BY sort"), books=q("SELECT * FROM books ORDER BY id DESC"), top=q("SELECT name,views FROM regions ORDER BY views DESC LIMIT 5"))

    @app.route("/admin/region/<slug>", methods=["GET", "POST"])
    @admin_required
    def admin_region(slug):
        d = db(); r = d.execute("SELECT * FROM regions WHERE slug=?", (slug,)).fetchone() or abort(404)
        if request.method == "POST":
            f = request.form; cover = save(request.files.get("cover"))
            d.execute("UPDATE regions SET capital=?,population=?,area=?,languages=?,about=?,history=?,culture=?,tourism=?,economy=?,food=?,climate=?,travel=? WHERE slug=?", tuple(f.get(k, "") for k in ["capital", "population", "area", "languages", "about", "history", "culture", "tourism", "economy", "food", "climate", "travel"]) + (slug,))
            if cover: d.execute("UPDATE regions SET cover=? WHERE slug=?", (cover, slug))
            d.commit(); flash("Region updated"); return redirect(url_for("region", slug=slug))
        return render_template("admin_region.html", r=r)

    @app.route("/admin/edit/<int:i>", methods=["GET", "POST"])
    @admin_required
    def admin_edit(i):
        d = db(); it = d.execute("SELECT * FROM items WHERE id=?", (i,)).fetchone() or abort(404)
        if request.method == "POST":
            f = request.form; fn = save(request.files.get("file"))
            if fn is False: flash("File type not allowed"); return redirect(request.url)
            d.execute("UPDATE items SET title=?,description=?,link=?,kind=?,zone=? WHERE id=?", (f["title"], f["description"], f.get("link"), f["kind"], f.get("zone") or None, i))
            if fn: d.execute("UPDATE items SET file=? WHERE id=?", (fn, i))
            d.commit(); flash("Updated"); return redirect(url_for("admin"))
        return render_template("admin_edit.html", it=it)

    def deleter(path, table):
        @app.route(f"/admin/{path}/<int:i>", methods=["POST"], endpoint="del_" + table)
        @admin_required
        def _d(i):
            db().execute(f"DELETE FROM {table} WHERE id=?", (i,)); db().commit(); return redirect(url_for("admin"))
    for p, t in [("comment", "comments"), ("message", "messages"), ("event", "events"), ("book", "books")]: deleter(p, t)
