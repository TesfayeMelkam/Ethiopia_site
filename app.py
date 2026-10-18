import os, sqlite3, uuid
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import extras, features, time

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = os.environ.get("ETH_SECRET", "change-this-secret")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
FAILS = {}
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
UPLOADS = os.path.join(BASE, "static", "uploads")
ALLOWED = {"png", "jpg", "jpeg", "gif", "webp", "pdf", "epub", "doc", "docx", "mp3", "mp4", "txt"}
ADMIN_USER = os.environ.get("ETH_ADMIN_USER", "admin")
PASS_HASH = generate_password_hash(os.environ.get("ETH_ADMIN_PASS", "admin123"))  # set ETH_ADMIN_PASS env var to change
DB = os.path.join(BASE, "ethiopia.db")

# slug, name, capital, population, area, languages, about, map x, y
REGIONS = [
 ("addis-ababa","Addis Ababa","Addis Ababa","~5.7 million","527 km²","Amharic, Oromo","Capital of Ethiopia and seat of the African Union. Sits at about 2,355 m, one of the highest capitals in the world. Landmarks: National Museum (home of Lucy), Merkato, Entoto Hill, Holy Trinity Cathedral.",300,255),
 ("tigray","Tigray","Mekelle","~7 million","50,000 km²","Tigrinya","Home to Aksum, the ancient kingdom, the obelisks of Aksum, Yeha temple and the rock-hewn churches of Gheralta.",250,70),
 ("afar","Afar","Semera","~2 million","72,000 km²","Afar","Contains the Danakil Depression, Erta Ale volcano and Dallol, among the hottest places on Earth; Hadar, where Lucy was found.",400,140),
 ("amhara","Amhara","Bahir Dar","~23 million","154,000 km²","Amharic","Lake Tana, the Blue Nile Falls, Lalibela rock-hewn churches, Gondar castles and the Simien Mountains.",220,170),
 ("benishangul-gumuz","Benishangul-Gumuz","Asosa","~1 million","50,000 km²","Berta, Gumuz, Shinasha","Western region with the Grand Ethiopian Renaissance Dam on the Blue Nile and rich gold resources.",150,230),
 ("dire-dawa","Dire Dawa","Dire Dawa","~0.5 million","1,213 km²","Oromo, Somali, Amharic","Charter city and railway hub between Addis Ababa and Djibouti, famous for the old railway town and Kefira market.",440,225),
 ("gambela","Gambela","Gambela","~0.5 million","25,000 km²","Anuak, Nuer","Lowland region with Gambela National Park and the Baro River.",110,320),
 ("harari","Harari","Harar","~0.25 million","334 km²","Harari, Oromo","Walled city of Jugol (UNESCO), known for 82 mosques, hyena feeding and coffee.",475,250),
 ("oromia","Oromia","Addis Ababa (Finfinne)","~40 million","284,000 km²","Afaan Oromo","Largest region. Bale Mountains, Wenchi crater lake, coffee origin (Kaffa/Jimma), Gadaa system (UNESCO).",300,320),
 ("sidama","Sidama","Hawassa","~4 million","7,000 km²","Sidama","Newest region (2020). Famous for Sidamo coffee, Lake Hawassa and the Fiche-Chambalaalla New Year festival.",300,385),
 ("somali","Somali","Jigjiga","~6 million","280,000 km²","Somali","Eastern region with vast pastoral lands, Shebelle and Genale rivers.",490,330),
 ("south-ethiopia","South Ethiopia","Arba Minch","~4 million","~36,000 km²","Wolaytatto, Gamo, Gofa, others","Lakes Abaya and Chamo, Nechisar National Park, Dorze and Konso cultural landscape.",235,375),
 ("central-ethiopia","Central Ethiopia","Hosaena","~8 million","~30,000 km²","Gurage, Hadiya, Kembata","Cultural home of Gurage, Hadiya and Kembata peoples; enset (false banana) agriculture, Tiya stelae.",260,330),
 ("south-west-ethiopia","South West Ethiopia","Bonga","~3 million","~25,000 km²","Kafa, Sheka, Bench","Birthplace of wild Arabica coffee in Kaffa forests (UNESCO biosphere).",180,360),
]
CHURCHES = {
 "amhara":[("Lalibela Rock-Hewn Churches","11 monolithic churches carved in the 12th–13th century under King Lalibela; UNESCO World Heritage Site; Bete Giyorgis is the most famous."),("Debre Berhan Selassie, Gondar","17th-century church famed for its ceiling of angel faces."),("Lake Tana Monasteries","Ancient island monasteries such as Ura Kidane Mihret and Narga Selassie.")],
 "tigray":[("Church of Our Lady Mary of Zion, Aksum","Said to house the Ark of the Covenant; one of the holiest Ethiopian Orthodox sites."),("Abuna Yemata Guh","Cliff church with 5th-century roots in Gheralta, reached by climbing."),("Debre Damo Monastery","6th-century monastery on a flat-topped amba, accessible only by rope.")],
 "addis-ababa":[("Holy Trinity Cathedral","Built 1941 for Ethiopia's victory; burial place of Emperor Haile Selassie."),("St. George Cathedral","Built 1896 after the Battle of Adwa, octagonal design."),("Entoto Maryam Church","Founded by Emperor Menelik II on Entoto Hill.")],
 "oromia":[("Adadi Mariam","Rock-hewn church south of Addis, attributed to the 12th century."),("Sheikh Hussein Shrine","Major pilgrimage site in Bale.")],
 "harari":[("Jami Mosque","Harar's great mosque, 16th century."),("Medhane Alem Cathedral","Orthodox cathedral in Harar.")],
 "dire-dawa":[("Saint Gabriel Church","Important Orthodox church in Dire Dawa.")],
 "sidama":[("Hawassa Saint Gabriel Church","Landmark church near Lake Hawassa.")],
}

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB); g.db.row_factory = sqlite3.Row
    return g.db
@app.teardown_appcontext
def close(e=None):
    d = g.pop("db", None)
    if d: d.close()

def init():
    from seed import ZONES, ITEMS
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS regions(slug TEXT PRIMARY KEY,name,capital,population,area,languages,about,x,y)")
    c.execute("CREATE TABLE IF NOT EXISTS zones(slug TEXT PRIMARY KEY,region,name,center,about,history,culture,tourism,economy)")
    c.execute("CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY AUTOINCREMENT,region TEXT,kind TEXT,title TEXT,description TEXT,file TEXT,link TEXT,zone TEXT)")
    if "zone" not in [r[1] for r in c.execute("PRAGMA table_info(items)")]:
        c.execute("ALTER TABLE items ADD COLUMN zone TEXT")
    if c.execute("SELECT COUNT(*) FROM regions").fetchone()[0] == 0:
        c.executemany("INSERT INTO regions VALUES(?,?,?,?,?,?,?,?,?)", REGIONS)
        for slug, lst in CHURCHES.items():
            for t, d in lst:
                c.execute("INSERT INTO items(region,kind,title,description) VALUES(?,?,?,?)", (slug,"church",t,d))
    if c.execute("SELECT COUNT(*) FROM zones").fetchone()[0] == 0:
        c.executemany("INSERT INTO zones VALUES(?,?,?,?,?,?,?,?,?)", ZONES)
        c.executemany("INSERT INTO items(region,zone,kind,title,description) VALUES(?,?,?,?,?)", ITEMS)
    c.commit(); c.close(); extras.setup_db(DB); features.setup_db(DB)

@app.context_processor
def inject():
    return {"all_regions": db().execute("SELECT slug,name FROM regions ORDER BY name").fetchall(), "all_zones": db().execute("SELECT slug,name,region FROM zones ORDER BY name").fetchall()}

@app.route("/search")
def search():
    q = request.args.get("q", "").strip(); like = f"%{q}%"; res = {"regions": [], "zones": [], "items": [], "books": []}
    if q:
        d = db()
        res["regions"] = d.execute("SELECT * FROM regions WHERE name LIKE ? OR about LIKE ? OR capital LIKE ?", (like,like,like)).fetchall()
        res["zones"] = d.execute("SELECT * FROM zones WHERE name LIKE ? OR about LIKE ? OR history LIKE ? OR culture LIKE ? OR tourism LIKE ? OR center LIKE ?", (like,)*6).fetchall()
        res["items"] = d.execute("SELECT i.*,r.name rname FROM items i JOIN regions r ON r.slug=i.region WHERE i.title LIKE ? OR i.description LIKE ?", (like,like)).fetchall()
        res["books"] = db().execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR description LIKE ?", (like,like,like)).fetchall()
    return render_template("search.html", q=q, res=res)

@app.route("/api/suggest")
def suggest():
    from flask import jsonify
    q = request.args.get("q", "").strip()
    if len(q) < 2: return jsonify([])
    d = db(); like = f"{q}%"
    names = [r[0] for r in d.execute("SELECT name FROM regions WHERE name LIKE ? UNION SELECT name FROM zones WHERE name LIKE ? UNION SELECT title FROM items WHERE title LIKE ? LIMIT 8", (like,like,like))]
    return jsonify(names)

@app.route("/regions")
def regions():
    return render_template("regions.html", regs=db().execute("SELECT * FROM regions ORDER BY name").fetchall())

def admin_required(f):
    @wraps(f)
    def w(*a, **k):
        if not session.get("admin"): return redirect(url_for("login"))
        return f(*a, **k)
    return w

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        ip, now = request.remote_addr, time.time(); FAILS[ip] = [x for x in FAILS.get(ip, []) if now - x < 600]
        if len(FAILS[ip]) >= 5:
            flash("Too many attempts. Try again in 10 minutes."); return render_template("login.html")
        if request.form["user"] == ADMIN_USER and check_password_hash(PASS_HASH, request.form["password"]):
            FAILS.pop(ip, None); session["admin"] = True; return redirect(url_for("admin"))
        FAILS[ip].append(now); flash("Wrong username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear(); return redirect(url_for("index"))

@app.route("/admin/delete-zone/<slug>", methods=["POST"])
@admin_required
def delete_zone(slug):
    db().execute("DELETE FROM zones WHERE slug=?", (slug,)); db().commit()
    return redirect(url_for("admin"))

@app.route("/admin/delete/<int:i>", methods=["POST"])
@admin_required
def delete(i):
    row = db().execute("SELECT file FROM items WHERE id=?", (i,)).fetchone()
    if row and row["file"]:
        p = os.path.join(UPLOADS, row["file"])
        if os.path.exists(p): os.remove(p)
    db().execute("DELETE FROM items WHERE id=?", (i,)); db().commit()
    return redirect(url_for("admin"))

@app.before_request
def csrf_protect():
    if "t" not in session: session["t"] = uuid.uuid4().hex
    if request.method == "POST" and request.endpoint != "static":
        tok = request.form.get("_csrf") or request.headers.get("X-CSRF")
        if not tok or tok != session.get("t"): abort(400)

extras.register(app, db, admin_required, UPLOADS, ALLOWED)
features.register(app, db, admin_required)

if __name__ == "__main__":
    os.makedirs(UPLOADS, exist_ok=True); init()
    port = int(os.environ.get("PORT", 5000))
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true" and not os.environ.get("ETH_NO_BROWSER"):
        import threading, webbrowser
        threading.Timer(1.5, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
    app.run(debug=True, port=port)
