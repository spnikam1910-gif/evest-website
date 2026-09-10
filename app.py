import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect

from config import config_by_name
from models import db, Lead, NewsletterSubscriber
from forms import ContactForm, SERVICE_CHOICES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evest")


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.environ.get("FLASK_ENV", "production")
    app.config.from_object(config_by_name.get(config_name, config_by_name["production"]))

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    CSRFProtect(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    register_error_handlers(app)
    return app


# ---------------------------------------------------------------------------
# Static site content. In a real deployment this could move to a CMS or a
# JSON/YAML data file — kept inline here so the whole site is easy to read
# and edit without touching templates.
# ---------------------------------------------------------------------------

COMPANY = {
    "name": "EVEST",
    "tagline": "Smart Solutions. Stronger Growth.",
    "phone": "+91 98765 43210",
    "email": "hello@evest.com",
    "address": "MG Road, Bengaluru, India",
}

STATS = [
    {"value": "500+", "label": "Clients served"},
    {"value": "95%", "label": "Client satisfaction"},
    {"value": "10+", "label": "Years in operation"},
    {"value": "24/7", "label": "Support coverage"},
]
# NOTE: placeholder figures — replace with EVEST's real numbers before launch.

SERVICES = [
    {
        "icon": "compass",
        "name": "Strategy Consulting",
        "slug": "strategy-consulting",
        "summary": "A clear-eyed read on where you stand and a practical plan to move forward.",
    },
    {
        "icon": "trending-up",
        "name": "Growth Marketing",
        "slug": "growth-marketing",
        "summary": "Demand generation and positioning built around measurable outcomes.",
    },
    {
        "icon": "bar-chart",
        "name": "Financial Advisory",
        "slug": "financial-advisory",
        "summary": "Forecasting, budgeting, and capital planning grounded in your numbers.",
    },
    {
        "icon": "settings",
        "name": "Business Automation",
        "slug": "business-automation",
        "summary": "Removing manual busywork from operations so your team can scale.",
    },
    {
        "icon": "layers",
        "name": "Brand Development",
        "slug": "brand-development",
        "summary": "A visual and verbal identity that earns trust before the first meeting.",
    },
]

WHY_EVEST = [
    {"icon": "award", "title": "Proven expertise", "text": "A decade of hands-on work across strategy, growth, and finance."},
    {"icon": "eye", "title": "A transparent process", "text": "You see the plan, the timeline, and the reasoning at every stage."},
    {"icon": "users", "title": "Built around you", "text": "Recommendations are shaped by your goals, not a one-size template."},
    {"icon": "life-buoy", "title": "Support that shows up", "text": "A direct line to your team, not a ticket queue."},
    {"icon": "zap", "title": "Practical innovation", "text": "New tools and methods, adopted only where they earn their place."},
    {"icon": "target", "title": "Judged by outcomes", "text": "We track the same results you do, and report on them plainly."},
]

PROCESS_STEPS = [
    {"step": "01", "title": "Connect", "text": "A short call to understand where you are and what you're solving for."},
    {"step": "02", "title": "Understand", "text": "We study your market, numbers, and operations before proposing anything."},
    {"step": "03", "title": "Build a Strategy", "text": "A concrete plan with milestones, owners, and a realistic timeline."},
    {"step": "04", "title": "Achieve Results", "text": "We execute alongside your team and adjust based on what the data shows."},
]

TESTIMONIALS = [
    {
        "name": "Ananya Rao",
        "role": "Founder, Northline Retail",
        "rating": 5,
        "quote": "EVEST rebuilt how we plan quarters. We finally make decisions from numbers instead of guesswork.",
        "placeholder": True,
    },
    {
        "name": "Marcus Webb",
        "role": "COO, Halden Logistics",
        "rating": 5,
        "quote": "The automation work alone paid for the engagement within four months.",
        "placeholder": True,
    },
    {
        "name": "Priya Nair",
        "role": "CEO, Fieldstone Consulting",
        "rating": 4,
        "quote": "Direct, well-organized, and honest about what would and wouldn't work for us.",
        "placeholder": True,
    },
]
# NOTE: placeholder testimonials — replace with verified customer quotes and
# photos before launch. Do not publish invented reviews as real.

FAQS = [
    {
        "q": "What industries does EVEST work with?",
        "a": "We work primarily with small and mid-sized businesses across retail, logistics, and professional services, though our strategy and financial advisory work applies broadly.",
    },
    {
        "q": "How long does a typical engagement take?",
        "a": "Most engagements run 8–12 weeks for the initial strategy phase, followed by an ongoing support arrangement if you'd like us to stay involved through execution.",
    },
    {
        "q": "Do you work with early-stage companies?",
        "a": "Yes. We adjust scope and pricing for early-stage teams — the process is the same, but engagements are typically shorter and more focused.",
    },
    {
        "q": "What happens after I submit the contact form?",
        "a": "A member of our team reviews your submission and reaches out within one business day to schedule an introductory call.",
    },
    {
        "q": "Is the first consultation free?",
        "a": "Yes, the initial consultation is complimentary and carries no obligation to continue.",
    },
    {
        "q": "Can EVEST support us remotely?",
        "a": "Most of our engagements run remotely with periodic on-site visits where useful. We can also work fully on-site if that fits your team better.",
    },
    {
        "q": "How is pricing structured?",
        "a": "Pricing depends on scope — we quote a fixed project fee after the first consultation rather than billing open-ended hourly rates.",
    },
]

NAV_LINKS = [
    ("Home", "home"),
    ("About", "about"),
    ("Services", "services"),
    ("Why EVEST", "why-evest"),
    ("Testimonials", "testimonials"),
    ("FAQ", "faq"),
    ("Contact", "contact"),
]


def register_routes(app):
    @app.context_processor
    def inject_globals():
        return {"company": COMPANY, "nav_links": NAV_LINKS, "current_year": datetime.utcnow().year}

    @app.route("/", methods=["GET"])
    def index():
        form = ContactForm()
        return render_template(
            "index.html",
            form=form,
            stats=STATS,
            services=SERVICES,
            why_evest=WHY_EVEST,
            process_steps=PROCESS_STEPS,
            testimonials=TESTIMONIALS,
            faqs=FAQS,
            page_title="EVEST — Smart Solutions. Stronger Growth.",
            meta_description="EVEST partners with growing businesses on strategy, growth marketing, "
            "financial advisory, and automation — practical plans, built around your numbers.",
        )

    @app.route("/contact", methods=["POST"])
    def contact():
        form = ContactForm()

        # Honeypot field: real users never fill this in, bots often do.
        if request.form.get("website"):
            logger.warning("Honeypot triggered on contact form; discarding submission.")
            flash("Thanks — we'll be in touch shortly.", "success")
            return redirect(url_for("index", _anchor="contact"))

        if form.validate_on_submit():
            lead = Lead(
                full_name=form.full_name.data.strip(),
                email=form.email.data.strip().lower(),
                phone=form.phone.data.strip(),
                company_name=(form.company_name.data or "").strip(),
                service_interested=dict(SERVICE_CHOICES).get(
                    form.service_interested.data, form.service_interested.data
                ),
                message=(form.message.data or "").strip(),
            )
            db.session.add(lead)
            db.session.commit()

            notify_new_lead(lead)

            flash("Thank you — your message has been sent. We'll reach out within one business day.", "success")
            return redirect(url_for("index", _anchor="contact"))

        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", "error")
        return redirect(url_for("index", _anchor="contact"))

    @app.route("/privacy-policy")
    def privacy():
        return render_template("privacy.html", page_title="Privacy Policy — EVEST")

    @app.route("/terms")
    def terms():
        return render_template("terms.html", page_title="Terms & Conditions — EVEST")

    @app.route("/healthz")
    def healthz():
        return jsonify({"status": "ok"})


def notify_new_lead(lead: Lead):
    """Hook for connecting new leads to email, a CRM, or WhatsApp.

    Currently a no-op unless MAIL_ENABLED / LEAD_WEBHOOK_URL are configured
    in .env — kept simple and explicit so it's obvious where to plug in a
    real provider (SendGrid, HubSpot, Twilio, Zapier, etc.) later.
    """
    from flask import current_app

    if current_app.config.get("MAIL_ENABLED"):
        logger.info("MAIL_ENABLED is set — wire up your mail provider here for lead #%s.", lead.id)

    webhook_url = current_app.config.get("LEAD_WEBHOOK_URL")
    if webhook_url:
        logger.info("LEAD_WEBHOOK_URL is set — POST lead #%s to %s here.", lead.id, webhook_url)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", page_title="Page Not Found — EVEST"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.exception("Internal server error")
        return render_template("500.html", page_title="Something Went Wrong — EVEST"), 500


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=app.config.get("DEBUG", False))
