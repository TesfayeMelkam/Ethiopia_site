# Ethiopia Information Portal (Flask)

## Run in PyCharm (3 steps)
1. File > Open > choose this folder. When PyCharm offers, create a virtualenv and install requirements.txt
   (or open the Terminal tab and run: pip install -r requirements.txt)
2. Right-click app.py > Run 'app'. The browser opens automatically at http://127.0.0.1:5000
3. Admin: http://127.0.0.1:5000/admin  (admin / admin123)

No PyCharm? Windows: double-click run.bat. Mac/Linux: sh run.sh

## Settings (environment variables, optional)
ETH_ADMIN_USER, ETH_ADMIN_PASS (admin login) | PORT (default 5000) | ETH_NO_BROWSER=1 (do not auto-open browser)
In PyCharm: Run > Edit Configurations > Environment variables.

## Features
Regions + zones + cities + churches + festivals | Library with online book reader and downloads | Know Ethiopia | Quiz
Trip planner | Saved places | Ctrl+K search | Amharic names | Installable app (PWA) | JSON API | Admin dashboard, backup export

NOTE: starting content is NOT verified against official sources. Check facts before publishing.

## New in v7
Map (Leaflet) + near me | live weather | EN/Amharic/Oromo menu | Learn Amharic | Recipes | People & history | Directory (owners submit, admin approves)
Stories + Poll + Newsletter | Kids page | Compare | Statistics | Open data (CSV/JSON) | Printable guides & worksheets | Quiz leaderboard
Accessibility (text size, contrast, low-data) | Voice search | CSRF protection, login rate limit, audit log | Bulk CSV import | Backup export
Deploy: pip install -r requirements-prod.txt, then: gunicorn wsgi:app (or use Procfile / Dockerfile). Set ETH_SECRET and ETH_ADMIN_PASS.
