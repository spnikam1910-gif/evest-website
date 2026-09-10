# EVEST — Business Website (Flask)

A premium, responsive business website for EVEST built with Flask, Jinja2,
vanilla CSS/JS, and SQLAlchemy. No build step required — everything runs
directly from Python.

## Project structure

```
evest/
├── app.py                 # Routes, app factory, lead-notification hook
├── config.py               # Env-based configuration (dev/production)
├── models.py                # SQLAlchemy models (Lead, NewsletterSubscriber)
├── forms.py                 # Flask-WTF contact form + server-side validation
├── requirements.txt
├── .env.example              # Copy to .env and fill in real values
├── static/
│   ├── css/style.css          # Full design system + responsive layout
│   ├── js/main.js              # Nav toggle, scroll reveal, form UX
│   └── img/                     # favicon + OG share image (SVG)
├── templates/
│   ├── base.html                # <head>, SEO meta, layout shell
│   ├── index.html                 # Home page — all sections
│   ├── privacy.html, terms.html    # Legal pages
│   ├── 404.html, 500.html            # Error pages
│   └── partials/
│       ├── navbar.html
│       ├── footer.html
│       └── icons.html               # Inline SVG icon macro (no CDN dependency)
└── instance/                          # SQLite DB lives here (auto-created)
```

## Run locally

1. **Create a virtual environment and install dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Open `.env` and set `SECRET_KEY` to a long random string (e.g. run
   `python -c "import secrets; print(secrets.token_hex(32))"`). The
   defaults otherwise work fine for local development with SQLite.

3. **Run the app**

   ```bash
   python app.py
   ```

   Visit `http://localhost:5000`. The SQLite database is created
   automatically in `instance/evest.db` on first run.

## Editing content

All site copy (stats, services, testimonials, FAQ, process steps) lives in
plain Python dictionaries near the top of `app.py`, so non-developers can
update wording without touching HTML. Two things are explicitly flagged as
placeholders and **must** be replaced before launch:

- `STATS` — placeholder numbers (500+ clients, 95% satisfaction, etc.)
- `TESTIMONIALS` — placeholder quotes marked `"placeholder": True`

## Connecting the contact form to email / CRM / WhatsApp

Form submissions are validated server-side (Flask-WTF + WTForms),
protected by CSRF tokens and a honeypot field, and saved to the `Lead`
table. To forward new leads elsewhere, open `app.py` and fill in the
`notify_new_lead()` function — it's called right after every successful
submission and already reads `MAIL_ENABLED` / `LEAD_WEBHOOK_URL` from your
`.env`. Typical options:

- **Email**: add Flask-Mail (or an API like SendGrid/Postmark) and send a
  notification to `LEAD_NOTIFICATION_EMAIL`.
- **CRM**: POST `lead.to_dict()` to your CRM's REST API.
- **WhatsApp**: POST to a Twilio/WhatsApp Business API webhook using
  `LEAD_WEBHOOK_URL`.

## Security notes

- CSRF protection is enabled globally via `Flask-WTF`'s `CSRFProtect`.
- All form input is validated server-side (never trust client-side
  validation alone); email/phone/length constraints live in `forms.py`.
- A hidden honeypot field (`website`) silently discards simple bot
  submissions.
- No secrets are hard-coded — `SECRET_KEY`, database URI, and any mail/CRM
  credentials are read from environment variables via `.env`
  (see `.env.example`). Make sure `.env` is never committed — it's already
  in `.gitignore`.
- Swap `SQLALCHEMY_DATABASE_URI` for a managed Postgres/MySQL instance in
  production; SQLite is intended for development only.

## Deploying

**Any standard Python host works** (Render, Railway, Fly.io, a VPS, etc.).
General steps:

1. Set `FLASK_ENV=production` and a strong `SECRET_KEY` in your host's
   environment variables — don't rely on `.env` in production; use the
   platform's secret manager.
2. Point `DATABASE_URL` at a managed database.
3. Run with a production WSGI server instead of the Flask dev server:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

4. Put a reverse proxy (Nginx, or your platform's built-in one) in front
   of Gunicorn, and serve `/static` with caching headers or a CDN for
   best performance.
5. Enable HTTPS (most platforms provide this automatically) — the site
   assumes it's served over HTTPS in production.

### Quick deploy examples

- **Render / Railway**: connect the repo, set the start command to
  `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`, add the environment
  variables from `.env.example` in the dashboard.
- **A plain VPS**: use Gunicorn behind Nginx with a systemd service, or
  containerize with a simple Dockerfile (`FROM python:3.12-slim`, copy
  the project, `pip install -r requirements.txt`, `CMD ["gunicorn", "-w",
  "4", "-b", "0.0.0.0:8000", "app:app"]`).

## Editable sections checklist before launch

- [ ] Replace placeholder stats in `app.py` → `STATS`
- [ ] Replace placeholder testimonials in `app.py` → `TESTIMONIALS`
- [ ] Update `COMPANY` (phone, email, address) in `app.py`
- [ ] Replace `static/img/favicon.svg` and `og-cover.svg` with real brand
      assets if desired
- [ ] Fill in `notify_new_lead()` with real email/CRM/WhatsApp integration
- [ ] Replace placeholder legal copy in `templates/privacy.html` and
      `templates/terms.html` with counsel-reviewed text
- [ ] Set a strong, unique `SECRET_KEY` in production
