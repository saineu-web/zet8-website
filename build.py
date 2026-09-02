"""Build the ZET8 multi-page site.

Generates:
  index.html                    home
  ponchi/ deskomigo/ crm/ localsave/ onsms/   product pages (index.html each)
  about/ contact/               company pages
  404.html, sitemap.xml         extras
  artifact-preview.html         single-file home variant with absolute links (not deployed)

Edit page copy / product data below, run  python build.py , then commit + push
(GitHub Pages redeploys zet8.com). Never hand-edit the generated files.
"""
import base64
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://zet8.com"

# ---------------------------------------------------------------- product data
PRODUCTS = [
    {
        "slug": "ponchi", "name": "Ponchi", "hue": "yellow", "cat": "Workforce",
        "domain": "ponchi.app", "url": "https://ponchi.app",
        "tagline": "Workforce management made simple.",
        "card": "Time clock, scheduling, and payroll-ready reports for hourly and on-site teams.",
        "about": "Time clock, scheduling, and payroll-ready reports for hourly and on-site teams — restaurants, retail, construction, healthcare, salons. Every punch honest, every shift covered.",
        "features": [
            ("Verified clock-in", "GPS and photo verification on every punch stops time theft before it starts."),
            ("Shift scheduling", "Build schedules in minutes; swaps and time-off requests handled in-app."),
            ("Payroll-ready exports", "Hours land clean and export-ready for whatever payroll you already use."),
            ("Live labor costs", "See labor cost in real time — before the week ends, not after."),
            ("Kiosk mode", "One shared tablet clocks in the whole crew at the door."),
            ("English + Español", "Fully bilingual, with team messaging and recognition built in."),
        ],
        "pricing": "From $9.99/mo · 14-day free trial · no card required",
    },
    {
        "slug": "deskomigo", "name": "Deskomigo", "hue": "green", "cat": "Back office",
        "domain": "deskomigo.com", "url": "https://deskomigo.com",
        "tagline": "Your office assistant, in your pocket.",
        "card": "Invoices, payments, bookings, receipts, and an AI assistant for service pros.",
        "about": "The back office for service pros — plumbers, electricians, HVAC, cleaners, landscapers. Invoices, payments, bookings, receipts, and an AI assistant, so the paperwork gets done from the truck.",
        "features": [
            ("Get paid on the spot", "Tap to Pay, payment links, or manual entry — collect before you leave the driveway."),
            ("Invoices & quotes", "Professional invoices and quotes generated in seconds, not evenings."),
            ("AI receipt scanning", "Snap a receipt; vendor, amount, tax, and category extracted automatically."),
            ("Bookings & deposits", "Customers book online and pay deposits, so no-shows cost them, not you."),
            ("Team & permissions", "Up to 5 users on Crew, each with exactly the access they should have."),
            ("Contracts & e-sign", "Digital contracts signed on the customer's phone, stored with the job."),
        ],
        "pricing": "From $29.99/mo · 14-day free trial · no card required",
    },
    {
        "slug": "huntcustomer", "name": "HuntCustomer", "hue": "blue", "cat": "Sales",
        "domain": "huntcustomer.com", "url": "https://huntcustomer.com",
        "tagline": "Intelligent targeting. Precision results.",
        "card": "A clean sales CRM for your team — or trained reps who do the hunting for you.",
        "about": "A sales platform two ways: run your own outbound with a clutter-free CRM — pipeline, contacts, quotes to invoices, team workspaces — or plug in trained sales reps who handle the cold calling and deliver meetings on a quota basis.",
        "features": [
            ("Visual pipeline", "Drag deals across stages you define. See what's stuck and what's closing."),
            ("Smart follow-ups", "Contacts carry automatic follow-up reminders, so leads stop going cold."),
            ("Sales reps on demand", "Dedicated or shared reps cold-call on a quota basis — pay per meetings delivered, not seats."),
            ("Quote → invoice → e-sign", "One workflow from the first number to the signed agreement."),
            ("Team workspaces", "Role-based permissions, shared calendars, and a dashboard of due items and stuck deals."),
            ("Cancel anytime", "Month-to-month billing. Stay because it works, not because you're locked in."),
        ],
        "pricing": "$14.99/user/mo · 14-day free trial · reps priced per quota",
    },
    {
        "slug": "localsave", "name": "LocalSave", "hue": "red", "cat": "Local commerce",
        "domain": "localsave.com", "url": "https://localsave.com",
        "tagline": "Local deals, local customers.",
        "card": "A hyperlocal deals platform connecting neighborhood businesses with shoppers nearby.",
        "about": "A hyperlocal deals platform that connects neighborhood businesses with shoppers nearby. Merchants publish deals from a simple dashboard; customers discover and redeem them from the app.",
        "features": [
            ("Deals near you", "Shoppers see offers from businesses in their own neighborhood, not national chains."),
            ("Merchant dashboard", "Publish a deal in minutes and track views and redemptions as they happen."),
            ("Mobile app", "Customers browse, save, and redeem deals straight from their phone."),
            ("English + Español", "Fully bilingual for merchants and shoppers alike."),
            ("Free to start", "Merchants list their business for free and upgrade only when it's working."),
            ("Built for main street", "Restaurants, salons, shops, services — the businesses that make a neighborhood."),
        ],
        "pricing": "Free for merchants to start · $14.99/mo to grow",
    },
    {
        "slug": "onsms", "name": "OnSMS", "hue": "green", "cat": "Hiring",
        "domain": "onsms.com", "url": "https://onsms.com",
        "tagline": "Text a job. Get offers. Pick one.",
        "card": "Text-based hiring — post a job by SMS, get sealed offers from workers, pick one.",
        "about": "Text-based hiring for businesses and homeowners who need workers now — shift coverage, cleaning, moving, construction, and more. Describe the job in a text, get sealed price offers from available workers, and pick one. Usually matched the same day.",
        "features": [
            ("Text a job", "Describe what you need in one message. Matching starts within minutes."),
            ("Sealed offers", "Available workers reply with their price. Compare offers and pick the best."),
            ("No app required", "Workers respond over plain SMS — no downloads, no sign-up friction."),
            ("Same-day matching", "Emergency staffing and shift coverage typically filled the same day."),
            ("Workers keep 100%", "Direct payment, no wage markup. Workers set their own rates."),
            ("English + Español", "Fully bilingual for employers and workers."),
        ],
        "pricing": "First 2 hires free · then $15 per confirmed hire",
    },
    {
        "slug": "initor", "name": "Initor", "hue": "blue", "cat": "Business launch",
        "domain": "initor.com", "url": "https://initor.com",
        "tagline": "Start your business in hours.",
        "card": "Describe your idea once — get your name, logo, plans, website, business card, LLC, and EIN in one click.",
        "about": "An AI business launcher. Describe your idea in one short paragraph and Initor generates your whole business at once — name, logo, business plan, marketing plan, website, and business card — then files your LLC and gets your EIN, so the business you just designed is a real, registered company.",
        "features": [
            ("Name & logo", "Brandable name ideas checked against live domain availability, plus a clean transparent-PNG logo in 5 style directions."),
            ("Real plans, not templates", "A 9-section business plan and an 8-section marketing plan grounded in your idea — downloadable as PDF or Word, fully editable."),
            ("A live website", "A professional one-page site generated and hosted for you. Edit any section with AI help and connect your own domain."),
            ("LLC & EIN included", "File your company in Texas, Delaware, or Wyoming with the EIN handled, so your new business is a real, registered company."),
            ("Business card", "A matching business card design generated with the rest of your brand."),
            ("You own everything", "Plans, logo, website content, and your domain are yours outright — in English or Español."),
        ],
        "pricing": "Free to start · no credit card to try",
    },
    {
        "slug": "luuky", "name": "Luuky", "hue": "red", "cat": "Coming soon",
        "domain": "luuky.com", "url": "https://luuky.com", "soon": True,
        "tagline": "Something new from ZET8.",
        "card": "The next ZET8 product is in the works. Details soon.",
        "about": "We're building the next member of the ZET8 family. What it does stays under wraps for now — but like everything we make, it'll be finished software a small business can just sign up for and use.",
        "features": [
            ("Under wraps", "We'll share what Luuky does closer to launch."),
            ("Built the ZET8 way", "Finished, mobile-first, bilingual — like the rest of the family."),
            ("Be first to know", "Write to us and we'll tell you the day it launches."),
        ],
        "pricing": "Coming soon",
    },
]

# Display order across the whole site (nav, scene stops, cards, sitemap).
# Lifecycle order — each app hands off to the next (the ecosystem story):
# start the business -> find customers -> local offers -> find workers ->
# manage workers/time -> run the money. Luuky (coming soon) closes the list.
_ORDER = ["initor", "huntcustomer", "localsave", "onsms", "ponchi", "deskomigo", "luuky"]
PRODUCTS.sort(key=lambda p: _ORDER.index(p["slug"]))

# ---------------------------------------------------------------------- css
CSS = """
  :root{
    --bg:#000000; --bg-2:#0c0c0c; --bg-3:#141414;
    --line:#202020; --line-2:#2c2c2c;
    --text:#EDEDED; --text-2:#B5B5B5; --muted:#737373; --cream:#F4F1EA;
    --green:#3CB371; --yellow:#F4C82D; --red:#E84A38; --blue:#5468E8;
    --radius:16px; --radius-lg:28px; --maxw:1140px;
    --ease:cubic-bezier(.2,.7,.2,1);
    --disp:"Space Grotesk",Bahnschrift,"Segoe UI",Arial,sans-serif;
    --body:Inter,"Segoe UI",Helvetica,Arial,sans-serif;
    --mono:"JetBrains Mono","Cascadia Code",Consolas,monospace;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth;scroll-padding-top:110px}
  @media(prefers-reduced-motion:reduce){
    html{scroll-behavior:auto}
    *{animation:none!important;transition:none!important}
    .reveal{opacity:1!important;transform:none!important}
  }
  body{background:var(--bg);color:var(--text);font-family:var(--body);font-size:16.5px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
  h1,h2,h3,h4{font-family:var(--disp);font-weight:700;line-height:1.08;letter-spacing:-.03em;color:var(--cream)}
  a{color:inherit;text-decoration:none}
  a:focus-visible,button:focus-visible{outline:2px solid var(--yellow);outline-offset:3px}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
  .mono{font-family:var(--mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
  .hue-green{--hue:var(--green);--hue-soft:rgba(60,179,113,.1)}
  .hue-yellow{--hue:var(--yellow);--hue-soft:rgba(244,200,45,.1)}
  .hue-red{--hue:var(--red);--hue-soft:rgba(232,74,56,.1)}
  .hue-blue{--hue:var(--blue);--hue-soft:rgba(84,104,232,.1)}

  .btn{display:inline-flex;align-items:center;gap:9px;padding:15px 26px;border-radius:100px;font-weight:600;font-size:.98rem;cursor:pointer;border:none;font-family:inherit;transition:.3s var(--ease)}
  .btn-primary{background:var(--yellow);color:#000}
  .btn-primary:hover{transform:translateY(-2px);box-shadow:0 14px 32px -10px rgba(244,200,45,.5)}
  .btn-ghost{background:transparent;color:var(--cream);border:1.5px solid var(--line-2)}
  .btn-ghost:hover{border-color:var(--cream)}
  .btn-hue{background:var(--hue);color:#000}
  .btn-hue:hover{transform:translateY(-2px)}
  .btn .arrow{transition:.25s}
  .btn:hover .arrow{transform:translateX(3px)}

  /* NAV */
  header{position:fixed;top:0;left:0;right:0;z-index:1000;transition:.4s var(--ease)}
  header.scrolled{background:rgba(0,0,0,.88);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
  nav{display:flex;align-items:center;justify-content:space-between;height:88px}
  .brand-img{height:42px;width:auto;display:block}
  .nav-links{display:flex;gap:26px;align-items:center}
  .nav-links a.lnk,.dd-btn{font-size:.93rem;font-weight:500;color:var(--text-2);transition:.2s;background:none;border:none;font-family:inherit;cursor:pointer;display:flex;align-items:center;gap:6px;padding:4px 0}
  .nav-links a.lnk:hover,.dd-btn:hover{color:var(--cream)}
  .nav-links a.lnk[aria-current="page"]{color:var(--cream)}
  .nav-links .btn{padding:12px 22px;font-size:.9rem}
  .dd{position:relative}
  .dd::after{content:"";position:absolute;top:100%;left:0;right:0;height:16px}
  .dd-btn .caret{font-size:.7rem;transition:.25s;color:var(--muted)}
  .dd.open .dd-btn .caret{transform:rotate(180deg)}
  .dd-menu{position:absolute;top:calc(100% + 14px);left:50%;transform:translateX(-50%);background:var(--bg-2);border:1px solid var(--line-2);border-radius:14px;padding:8px;min-width:250px;display:none;box-shadow:0 24px 60px rgba(0,0,0,.6);z-index:50}
  .dd.open .dd-menu,.dd:hover .dd-menu,.dd:focus-within .dd-menu{display:block}
  .dd-menu a{display:flex;align-items:center;gap:10px;padding:11px 12px;border-radius:9px;font-size:.92rem;color:var(--text-2);transition:.15s}
  .dd-menu a:hover{background:var(--bg-3);color:var(--cream)}
  .dd-menu .dot{width:8px;height:8px;border-radius:50%;background:var(--hue);flex-shrink:0}
  .dd-menu small{font-family:var(--mono);font-size:.62rem;color:var(--muted);margin-left:auto;letter-spacing:.04em}
  .hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:8px}
  .hamburger span{width:24px;height:2px;background:var(--cream);border-radius:2px}

  /* SCROLL SCENE (home) — camera journey along the "8". All scene chrome is
     hidden unless JS enables it via html.scene-on; no-WebGL / reduced-motion
     visitors get the static .scene-fallback hero instead. */
  #scene{position:fixed;inset:0;width:100%;height:100%;display:none;z-index:0}
  .vignette{display:none;position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 62% 50%,transparent 30%,rgba(0,0,0,.72) 78%,#000 100%)}
  .stage{display:none;position:fixed;inset:0;z-index:4;pointer-events:none}
  .runway{display:none;position:relative;z-index:2}
  .runway div{height:100vh}
  @supports(height:100svh){.runway div{height:100svh}}
  .hud,.minimap,.srail{display:none}
  .scene-on #scene,.scene-on .vignette,.scene-on .stage,.scene-on .runway,.scene-on .minimap,.scene-on .srail{display:block}
  .scene-on .hud{display:flex}
  .scene-on .scene-fallback{display:none}
  .scard{position:absolute;top:50%;left:clamp(20px,7vw,88px);transform:translateY(-50%);width:min(460px,78vw);opacity:0;visibility:hidden}
  .scard.on{visibility:visible}
  .scard .eyebrow2{font-family:var(--mono);font-size:.66rem;letter-spacing:.26em;text-transform:uppercase;color:var(--hue,var(--yellow));margin-bottom:18px;display:flex;gap:12px;align-items:center}
  .scard .eyebrow2::before{content:"";width:26px;height:1px;background:var(--hue,var(--yellow));display:block;flex:none}
  .scard h2{font-family:var(--disp);font-weight:700;font-size:clamp(34px,5vw,56px);line-height:1;letter-spacing:-.02em;margin-bottom:16px;color:var(--cream)}
  .scard h2 em{font-style:normal;color:var(--hue,var(--yellow))}
  .scard p{font-size:.95rem;line-height:1.65;color:var(--text-2);max-width:40ch}
  .scard .meta{margin-top:22px;font-family:var(--mono);font-size:.66rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;align-items:center}
  .scard .meta a{color:var(--cream);text-decoration:none;border-bottom:1px solid var(--hue,var(--yellow));padding-bottom:2px;pointer-events:auto}
  .scard .meta a:hover{color:var(--hue,var(--yellow))}
  .badge2{border:1px solid var(--line-2);padding:4px 9px;color:var(--muted)}
  .scard-center{left:50%;transform:translate(-50%,-50%);text-align:center;width:min(720px,86vw)}
  .scard-center .eyebrow2{justify-content:center}
  .scard-center p{max-width:52ch;margin-inline:auto}
  .scard-center .meta{justify-content:center}
  .swordmark-img{width:min(520px,78vw);height:auto;display:block;margin:0 auto;filter:drop-shadow(0 24px 60px rgba(0,0,0,.6))}
  .cue{margin-top:38px;font-family:var(--mono);font-size:.66rem;letter-spacing:.26em;text-transform:uppercase;color:var(--muted)}
  .cue i{display:inline-block;animation:drift 2.4s ease-in-out infinite;font-style:normal}
  @keyframes drift{0%,100%{transform:translateY(0);opacity:.5}50%{transform:translateY(5px);opacity:1}}
  .slinks{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:30px}
  .slinks a{pointer-events:auto;text-decoration:none;font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--cream);border:1px solid var(--line-2);padding:11px 16px;transition:.2s}
  .slinks a:hover{border-color:var(--yellow);color:var(--yellow)}
  .hud{position:fixed;left:clamp(20px,5vw,54px);bottom:34px;z-index:5;font-family:var(--mono);font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);pointer-events:none;gap:18px;align-items:baseline}
  .hud b{color:var(--yellow);font-weight:500}
  .minimap{position:fixed;right:clamp(20px,5vw,54px);bottom:26px;z-index:5;pointer-events:none;opacity:.9}
  .minimap svg{display:block;overflow:visible}
  .minimap .track{fill:none;stroke:rgba(244,200,45,.25);stroke-width:1}
  .minimap .dot{fill:var(--yellow)}
  .srail{position:fixed;left:0;bottom:0;height:2px;width:100%;z-index:5;background:rgba(244,241,234,.08)}
  .srail i{display:block;height:100%;width:0;background:var(--yellow);box-shadow:0 0 12px var(--yellow)}
  .scene-done .hud,.scene-done .minimap,.scene-done .srail{opacity:0;transition:opacity .5s}
  .after-scene{position:relative;z-index:6;background:var(--bg)}
  footer{position:relative;z-index:6;background:var(--bg)}

  .reveal{opacity:0;transform:translateY(26px);transition:.8s var(--ease)}
  .reveal.in{opacity:1;transform:none}
  .d1{transition-delay:.06s}.d2{transition-delay:.13s}.d3{transition-delay:.2s}.d4{transition-delay:.27s}

  section{padding:96px 0;position:relative}
  .sec-head{max-width:720px;margin-bottom:44px}
  .sec-head h2{font-size:clamp(1.8rem,4vw,2.9rem);margin:14px 0}
  .sec-head p{color:var(--text-2);font-size:1.05rem;max-width:600px}
  .eyebrow{display:inline-flex;align-items:center;gap:10px}
  .eyebrow .dot{width:9px;height:9px;border-radius:50%;display:inline-block}

  /* PRODUCTS strip (home, after the scene) */
  #products{background:var(--bg-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
  /* home lineup doubles as the lifecycle flow: numbered step on each card */
  .mini i{font-family:var(--mono);font-style:normal;font-size:.68rem;color:var(--hue);letter-spacing:.1em;display:block;margin-bottom:9px}
  .mini i::after{content:" →";color:var(--line-2)}
  .mini:last-child i::after{content:""}

  /* WHY strip */
  #why{padding:88px 0}
  .proc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .proc-card{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--radius);padding:28px}
  .proc-n{font-family:var(--mono);font-size:.76rem;letter-spacing:.08em;margin-bottom:12px}
  .proc-card:nth-child(1) .proc-n{color:var(--green)}
  .proc-card:nth-child(2) .proc-n{color:var(--yellow)}
  .proc-card:nth-child(3) .proc-n{color:var(--red)}
  .proc-card h4{font-size:1.28rem;margin-bottom:8px}
  .proc-card p{color:var(--text-2);font-size:.93rem}

  /* CTA band */
  .cta-band{border-top:1px solid var(--line);background:var(--bg-2);text-align:center;padding:84px 0}
  .cta-band h2{font-size:clamp(1.8rem,4.5vw,3rem);margin-bottom:14px}
  .cta-band p{color:var(--text-2);max-width:480px;margin:0 auto 30px}

  /* PRODUCT PAGE */
  .phero{padding:160px 0 70px;border-bottom:1px solid var(--line);position:relative;overflow:hidden}
  .phero::before{content:"";position:absolute;width:560px;height:560px;border-radius:50%;filter:blur(90px);opacity:.13;background:var(--hue);top:-200px;right:-160px;pointer-events:none}
  .crumbs{font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;color:var(--muted);margin-bottom:26px;text-transform:uppercase}
  .crumbs a:hover{color:var(--cream)}
  .crumbs .sep{margin:0 8px;color:var(--line-2)}
  .phero .tag{display:inline-block;font-family:var(--mono);font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px;border-radius:5px;color:var(--hue);background:var(--hue-soft);margin-bottom:16px}
  .phero h1{font-size:clamp(2.2rem,5.5vw,3.8rem);max-width:760px}
  .phero .tagline{font-family:var(--disp);font-weight:600;font-size:clamp(1.2rem,2.6vw,1.7rem);color:var(--hue);margin:10px 0 18px;letter-spacing:-.02em}
  .phero .about{color:var(--text-2);max-width:640px;font-size:1.06rem;margin-bottom:32px}
  .phero .cta-row{display:flex;gap:13px;flex-wrap:wrap}
  .phero .dom{display:block;font-family:var(--mono);font-size:.76rem;color:var(--muted);margin-top:22px;letter-spacing:.05em}

  .feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
  .feature{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px;transition:.3s var(--ease)}
  .feature:hover{border-color:var(--hue)}
  .feature b{font-family:var(--disp);font-weight:600;font-size:1rem;color:var(--cream);margin-bottom:6px;display:flex;align-items:center;gap:9px}
  .feature b::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--hue);flex-shrink:0}
  .feature span{font-size:.89rem;color:var(--text-2);line-height:1.5}

  .price-strip{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--bg-2);padding:44px 0}
  .price-row{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
  .price-row .p{font-family:var(--disp);font-weight:600;font-size:1.25rem;color:var(--cream);letter-spacing:-.02em}
  .price-row .p b{color:var(--hue)}

  .family h2{font-size:clamp(1.6rem,3.5vw,2.4rem);margin-bottom:30px}
  .mini-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
  .mini{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--radius);padding:20px;transition:.3s var(--ease)}
  .mini:hover{border-color:var(--hue);transform:translateY(-3px)}
  .mini b{display:flex;align-items:center;gap:9px;font-family:var(--disp);font-weight:600;color:var(--cream);font-size:1.02rem;margin-bottom:5px}
  .mini b::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--hue)}
  .mini span{font-size:.82rem;color:var(--muted)}

  /* ABOUT / CONTACT pages */
  .page-hero{padding:160px 0 60px}
  .page-hero h1{font-size:clamp(2.1rem,5vw,3.6rem);max-width:820px;margin:14px 0 18px}
  .page-hero .lead{color:var(--text-2);font-size:1.1rem;max-width:640px}
  .prose{max-width:680px;color:var(--text-2);font-size:1.02rem;display:flex;flex-direction:column;gap:18px}
  .prose b{color:var(--cream)}
  .legal-note{font-family:var(--mono);font-size:.74rem;color:var(--muted);letter-spacing:.04em;margin-top:26px}

  .contact-grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:50px;align-items:start}
  .cinfo .row{display:flex;gap:13px;align-items:center;margin-bottom:14px}
  .cinfo .ico{width:44px;height:44px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;flex-shrink:0;color:#000;font-weight:700}
  .cinfo .row:nth-child(1) .ico{background:var(--green)}
  .cinfo .row:nth-child(2) .ico{background:var(--yellow)}
  .cinfo b{color:var(--cream);display:block;font-size:.95rem}
  .cinfo span{color:var(--muted);font-size:.85rem}
  .form{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--radius-lg);padding:32px}
  .form .field{margin-bottom:15px}
  .form label{display:block;font-size:.74rem;color:var(--text-2);margin-bottom:6px;font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase}
  .form input,.form select,.form textarea{width:100%;padding:13px 15px;border:1.5px solid var(--line);border-radius:11px;font-family:inherit;font-size:.95rem;background:var(--bg-3);color:var(--text);transition:.25s}
  .form input::placeholder,.form textarea::placeholder{color:#555}
  .form input:focus,.form select:focus,.form textarea:focus{outline:none;border-color:var(--yellow)}
  .form .two{display:grid;grid-template-columns:1fr 1fr;gap:13px}
  .form textarea{resize:vertical;min-height:96px}
  .form .btn{width:100%;justify-content:center;margin-top:4px}
  .form-success{display:none;text-align:center;padding:30px 8px}
  .form-success.show{display:block}
  .form-success .check{width:60px;height:60px;border-radius:50%;background:var(--green);color:#000;display:flex;align-items:center;justify-content:center;font-size:1.9rem;margin:0 auto 16px;font-weight:700}
  .form-success h3{font-size:1.4rem;margin-bottom:7px}
  .form-success p{color:var(--text-2);font-size:.93rem}

  /* FOOTER */
  footer{border-top:1px solid var(--line);padding:44px 0 34px}
  .foot{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
  .foot .links{display:flex;gap:22px;font-size:.9rem;color:var(--text-2);flex-wrap:wrap}
  .foot .links a:hover{color:var(--cream)}
  .foot-bottom{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-top:26px;padding-top:22px;border-top:1px solid var(--line);color:var(--muted);font-size:.82rem}
  .color-bar{display:flex;height:4px;border-radius:2px;overflow:hidden;width:80px}
  .color-bar span{flex:1}
  .color-bar span:nth-child(1){background:var(--green)}
  .color-bar span:nth-child(2){background:var(--yellow)}
  .color-bar span:nth-child(3){background:var(--red)}
  .color-bar span:nth-child(4){background:var(--blue)}

  @media(max-width:900px){
    .scard{top:auto;bottom:112px;transform:none;left:24px;right:24px;width:auto}
    .scard-center{left:50%;right:auto;bottom:auto;top:50%;transform:translate(-50%,-50%);width:min(720px,86vw)}
    .scard p{max-width:none}
    .minimap{display:none!important}
    .proc-grid,.feature-grid{grid-template-columns:1fr}
    .mini-cards{grid-template-columns:1fr 1fr}
    .contact-grid{grid-template-columns:1fr;gap:34px}
    .nav-links{position:fixed;top:88px;left:0;right:0;background:var(--bg);flex-direction:column;align-items:stretch;padding:24px;gap:18px;border-bottom:1px solid var(--line);transform:translateY(-160%);transition:.4s var(--ease)}
    .nav-links.open{transform:none}
    .hamburger{display:flex}
    .dd::after{display:none}
    .dd-menu{position:static;transform:none;display:none;box-shadow:none;border:none;background:transparent;min-width:0;padding:4px 0 0 14px}
    .dd:hover .dd-menu{display:none}
    .dd.open .dd-menu{display:block}
    .form .two{grid-template-columns:1fr}
    .nav-links .btn{justify-content:center}
  }
  @media(max-width:560px){.mini-cards{grid-template-columns:1fr}}
"""

# ------------------------------------------------------------------- shared JS
JS = """
  (function () {
    var header = document.getElementById('header');
    window.addEventListener('scroll', function () { header.classList.toggle('scrolled', window.scrollY > 20); });

    var ham = document.getElementById('hamburger'), links = document.getElementById('navLinks');
    ham.addEventListener('click', function () { links.classList.toggle('open'); });
    links.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { links.classList.remove('open'); }); });

    var dd = document.getElementById('dd');
    var ddBtn = document.getElementById('ddBtn');
    ddBtn.addEventListener('click', function (e) { e.stopPropagation(); dd.classList.toggle('open'); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) dd.classList.remove('open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') dd.classList.remove('open'); });

    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .1 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  })();
"""

FORM_JS = """
  document.getElementById('quoteForm').addEventListener('submit', function (ev) {
    ev.preventDefault();
    var v = function (id) { return document.getElementById(id).value.trim(); };
    var subject = encodeURIComponent('ZET8 — ' + (v('need') || 'New inquiry'));
    var body = encodeURIComponent('Name: ' + v('name') + '\\nCompany: ' + v('biz') + '\\nEmail: ' + v('email') + '\\nNeed: ' + v('need') + '\\n\\nDetails:\\n' + v('msg'));
    window.location.href = 'mailto:hello@zet8.com?subject=' + subject + '&body=' + body;
    this.style.display = 'none';
    document.getElementById('formSuccess').classList.add('show');
  });
"""


def nav(logo_b64, current=""):
    items = "".join(
        '<a class="hue-%s" href="/%s/"><span class="dot"></span>%s<small>%s</small></a>'
        % (p["hue"], p["slug"], p["name"],
           "coming soon" if p.get("soon") else p["domain"]) for p in PRODUCTS
    )
    def cur(page):
        return ' aria-current="page"' if current == page else ""
    return """
<header id="header">
  <div class="wrap">
    <nav>
      <a href="/" aria-label="ZET8 home"><img class="brand-img" src="data:image/png;base64,%s" alt="ZET8"></a>
      <div class="nav-links" id="navLinks">
        <div class="dd" id="dd">
          <button class="dd-btn" id="ddBtn" aria-haspopup="true">Products <span class="caret">▼</span></button>
          <div class="dd-menu">%s</div>
        </div>
        <a href="/about/" class="lnk"%s>About Us</a>
        <a href="/contact/" class="btn btn-primary">Contact Us</a>
      </div>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>
""" % (logo_b64, items, cur("about"))


def footer():
    plinks = "".join('<a href="/%s/">%s</a>' % (p["slug"], p["name"]) for p in PRODUCTS)
    return """
<footer>
  <div class="wrap">
    <div class="foot">
      <div class="links">%s<a href="/about/">About Us</a><a href="/contact/">Contact Us</a></div>
      <div class="color-bar"><span></span><span></span><span></span><span></span></div>
    </div>
    <div class="foot-bottom"><span>© 2026 ZET8 · all rights reserved</span><span>Houston, Texas · zet8.com</span></div>
  </div>
</footer>
""" % plinks


def head(title, desc, path):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%(desc)s">
<title>%(title)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" href="/favicon-8.png">
<link rel="apple-touch-icon" href="/favicon-8.png">
<meta property="og:type" content="website">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(site)s%(path)s">
<meta property="og:image" content="%(site)s/logo-wide.png">
<meta property="og:site_name" content="ZET8">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(site)s/logo-wide.png">
<link rel="canonical" href="%(site)s%(path)s">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ZET8",
  "url": "%(site)s",
  "logo": "%(site)s/logo.png",
  "description": "ZET8 makes finished, ready-to-use apps for small businesses — Ponchi workforce management, Deskomigo mobile back office, HuntCustomer sales CRM, LocalSave local deals, OnSMS text-based hiring, and Initor business launch.",
  "email": "hello@zet8.com",
  "address": {"@type": "PostalAddress","addressLocality": "Houston","addressRegion": "TX","addressCountry": "US"},
  "parentOrganization": {"@type": "Organization","name": "Optima Buildsolutions LLC"},
  "sameAs": ["https://ponchi.app","https://deskomigo.com","https://huntcustomer.com","https://localsave.com","https://onsms.com","https://initor.com"]
}
</script>
<style>%(css)s</style>
<script defer src="https://stats.zet8.com/pulse.js" data-app="zet8"></script>
</head>
<body>
""" % {"title": title, "desc": desc, "path": path, "site": SITE, "css": CSS}


def page(title, desc, path, content, logo_b64, current="", extra_js=""):
    return (head(title, desc, path) + nav(logo_b64, current) + content + footer()
            + "<script>" + JS + extra_js + "</script>\n</body>\n</html>\n")


# ----------------------------------------------------------------- home page
HUE_HEX = {"green": "#3CB371", "yellow": "#F4C82D", "red": "#E84A38", "blue": "#5468E8"}

# Each product's role in the lifecycle — shown on journey stops and the
# ecosystem flow strip ("an operating system for small businesses").
STEP = {
    "initor":       "Start the business",
    "huntcustomer": "Find & manage customers",
    "localsave":    "Bring customers through the door",
    "onsms":        "Find workers",
    "ponchi":       "Manage the crew & the clock",
    "deskomigo":    "Run the money & back office",
    "luuky":        "The next part of the system",
}

# Scene-card headlines: one punchy line per stop, <em> takes the product hue.
PUNCH = {
    "ponchi":    "Clock in from<br>the <em>job site</em>.",
    "deskomigo": "Run the back office<br>from the <em>truck</em>.",
    "huntcustomer": "Hunt customers,<br>not <em>spreadsheets</em>.",
    "localsave": "Deals from the shop<br><em>down the street</em>.",
    "onsms":     "Post a job by<br><em>text message</em>.",
    "initor":    "Start the company<br><em>this week</em>.",
    "luuky":     "Something new is<br><em>on the way</em>.",
}


def home_content(logo_b64):
    import json
    live = sum(1 for p in PRODUCTS if not p.get("soon"))
    live_word = {4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}[live]
    scards = "".join("""
  <section class="scard hue-%s" data-step="%d">
    <div class="eyebrow2">%s · %s</div>
    <h2>%s</h2>
    <p>%s</p>
    <div class="meta"><span class="badge2">%s</span>%s</div>
  </section>""" % (p["hue"], i + 1, p["name"], STEP[p["slug"]], PUNCH[p["slug"]], p["card"],
                   p["pricing"],
                   '<a href="/contact/">Get notified</a>' if p.get("soon") else
                   '<a href="%s" target="_blank" rel="noopener">%s</a>' % (p["url"], p["domain"]))
                     for i, p in enumerate(PRODUCTS))
    outro_links = "".join('<a href="/%s/">%s</a>' % (p["slug"], p["name"]) for p in PRODUCTS)
    # The lineup IS the flow: numbered lifecycle steps, one card per product.
    minis = "".join(
        '<a class="mini hue-%s" href="/%s/"><i>%02d</i><b>%s</b><span>%s</span></a>'
        % (p["hue"], p["slug"], i + 1, p["name"], STEP[p["slug"]])
        for i, p in enumerate(PRODUCTS))
    data = json.dumps([{
        "name": p["name"], "cat": p["cat"], "tagline": p["tagline"],
        "pricing": p["pricing"],
        "domain": "coming soon" if p.get("soon") else p["domain"],
        "url": p["url"],
        "hex": HUE_HEX[p["hue"]], "features": [f[0] for f in p["features"][:4]],
    } for p in PRODUCTS])
    out = """
<canvas id="scene" aria-hidden="true"></canvas>
<div class="vignette"></div>

<div class="stage" id="stage">
  <section class="scard scard-center on" data-step="0">
    <div class="eyebrow2">One account · @@COUNT@@ products</div>
    <img class="swordmark-img" src="data:image/png;base64,%s" alt="ZET8">
    <p style="margin-top:26px">Ready-to-use apps for the businesses that actually run a city — the crews, the counters, the routes, and the people who own them.</p>
    <div class="cue">Scroll to travel the eight <i>↓</i></div>
  </section>
%s
  <section class="scard scard-center" data-step="%d">
    <div class="eyebrow2">End of track</div>
    <h2>An operating system<br>for <em>small business</em>.</h2>
    <p>Apps that hand off to each other — from the day you start the company to the day you get paid. Built in Houston, in the two languages this city runs on.</p>
    <div class="slinks">%s<a href="#products">Keep scrolling ↓</a></div>
  </section>
</div>

<div class="hud">
  <span>Track <b id="hudU">0.000</b></span>
  <span>Node <b id="hudN">00</b>/0%d</span>
</div>
<div class="minimap">
  <svg width="86" height="46" viewBox="0 0 86 46">
    <path id="mmPath" class="track"></path>
    <circle id="mmDot" class="dot" r="2.6" cx="0" cy="0"></circle>
  </svg>
</div>
<div class="srail"><i id="railFill"></i></div>

<main class="runway" id="top">%s</main>

<div class="scene-fallback">
  <section class="page-hero">
    <div class="wrap">
      <div class="eyebrow mono"><span class="dot" style="background:var(--yellow)"></span>Tech solutions for businesses</div>
      <h1>Ready-to-use apps that run your small business.</h1>
      <p class="lead">No custom builds, no six-month projects. ZET8 makes finished software products — sign up and start today.</p>
    </div>
  </section>
</div>

<div class="after-scene">
  <section id="products">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="eyebrow mono"><span class="dot" style="background:var(--yellow)"></span>The system</div>
        <h2>An operating system for small business.</h2>
        <p>Each app hands off to the next — from the day you start the company to the day you get paid.</p>
      </div>
      <div class="mini-cards">%s</div>
    </div>
  </section>

  <section id="why">
    <div class="wrap">
      <div class="sec-head reveal" style="margin-bottom:36px">
        <div class="eyebrow mono"><span class="dot" style="background:var(--red)"></span>Why ZET8</div>
        <h2>Finished software. No projects, no waiting.</h2>
      </div>
      <div class="proc-grid">
        <div class="proc-card reveal d1"><div class="proc-n">01 / Ready today</div><h4>Sign up, not scope out.</h4><p>Every ZET8 app is a finished product with a free trial. No quotes, no six-month builds — create an account and start working.</p></div>
        <div class="proc-card reveal d2"><div class="proc-n">02 / Built for small business</div><h4>Priced like tools, not platforms.</h4><p>Designed for owners with fifty jobs on the board, not fifty people in IT. Simple monthly pricing, cancel anytime.</p></div>
        <div class="proc-card reveal d3"><div class="proc-n">03 / One family</div><h4>Apps that work the same way.</h4><p>Mobile-first, bilingual, AI where it erases busywork. Learn one ZET8 app and the next one already feels familiar.</p></div>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap reveal">
      <h2>Not sure which app fits?</h2>
      <p>Tell us how your business runs and we'll point you to the right tool — a person answers.</p>
      <a href="/contact/" class="btn btn-primary">Contact us <span class="arrow">→</span></a>
    </div>
  </section>
</div>

<script>window.ZET8_PRODUCTS = %s;</script>
<script defer src="/assets/scene.js"></script>""" % (
        logo_b64, scards, len(PRODUCTS) + 1, outro_links, len(PRODUCTS),
        "<div></div>" * (len(PRODUCTS) + 2), minis, data)
    return out.replace("@@COUNT@@", live_word)


# -------------------------------------------------------------- product pages
def product_content(p):
    feats = "".join('<div class="feature reveal"><b>%s</b><span>%s</span></div>' % f for f in p["features"])
    minis = "".join("""
      <a class="mini hue-%s" href="/%s/"><b>%s</b><span>%s</span></a>""" % (
        q["hue"], q["slug"], q["name"], q["cat"]) for q in PRODUCTS if q["slug"] != p["slug"])
    return """
<div class="hue-%(hue)s">
<section class="phero">
  <div class="wrap">
    <div class="crumbs reveal"><a href="/">Home</a><span class="sep">/</span><a href="/#products">Products</a><span class="sep">/</span>%(name)s</div>
    <span class="tag reveal">%(cat)s</span>
    <h1 class="reveal d1">%(name)s</h1>
    <p class="tagline reveal d1">%(tagline)s</p>
    <p class="about reveal d2">%(about)s</p>
    <div class="cta-row reveal d3">
      %(cta_primary)s
      <a class="btn btn-ghost" href="/contact/">Ask a question</a>
    </div>
    <span class="dom reveal d4">%(pricing)s</span>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal"><div class="eyebrow mono"><span class="dot" style="background:var(--hue)"></span>Features</div><h2>What you get</h2></div>
    <div class="feature-grid">%(feats)s</div>
  </div>
</section>

<section class="price-strip">
  <div class="wrap price-row reveal">
    <span class="p">%(pricing_html)s</span>
    %(cta_strip)s
  </div>
</section>

<section class="family">
  <div class="wrap">
    <h2 class="reveal">More from ZET8</h2>
    <div class="mini-cards">%(minis)s</div>
  </div>
</section>
</div>
""" % {
        "hue": p["hue"], "name": p["name"], "cat": p["cat"], "tagline": p["tagline"],
        "about": p["about"], "pricing": p["pricing"],
        "pricing_html": p["pricing"].replace("·", "<b>·</b>"),
        "cta_primary": ('<a class="btn btn-hue" href="/contact/">Get notified <span class="arrow">→</span></a>'
                        if p.get("soon") else
                        '<a class="btn btn-hue" href="%s" target="_blank" rel="noopener">Visit %s <span class="arrow">→</span></a>'
                        % (p["url"], p["domain"])),
        "cta_strip": ('<a class="btn btn-hue" href="/contact/">Get notified <span class="arrow">→</span></a>'
                      if p.get("soon") else
                      '<a class="btn btn-hue" href="%s" target="_blank" rel="noopener">Get started <span class="arrow">→</span></a>'
                      % p["url"]),
        "feats": feats, "minis": minis,
    }


# -------------------------------------------------------------- about/contact
ABOUT = """
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow mono reveal"><span class="dot" style="background:var(--green)"></span>About us</div>
    <h1 class="reveal d1">Software for the businesses that keep the real economy moving.</h1>
    <p class="lead reveal d2">ZET8 is a Houston-based software company. We make finished, ready-to-use apps for small businesses — the restaurants, crews, shops, and service pros that big software forgets.</p>
  </div>
</section>
<section style="padding-top:20px">
  <div class="wrap">
    <div class="prose reveal" style="margin-bottom:52px">
      <div class="eyebrow mono" style="margin-bottom:6px"><span class="dot" style="background:var(--yellow)"></span>Why &ldquo;ZET8&rdquo;</div>
      <p><b>The name zet8 starts at the end.</b> Zet is how much of the world says the letter Z — the last stop in the alphabet, the point where the list of names runs out. The 8, tipped on its side, is ∞. Put them together and you get the whole idea in four characters: begin where everyone else stops, and keep going.</p>
      <p>We named the company after the space past the last letter — the problems that don't have a tidy label yet, the work that starts where the map ends. Everything we build lives out there.</p>
    </div>
    <div class="prose reveal">
      <p><b>We don't do custom projects.</b> Every ZET8 product is a finished app you can sign up for today — born from real problems we watched real businesses fight: time theft on job sites, invoices written at midnight, leads going cold in spreadsheets, empty shifts with no one to call.</p>
      <p><b>We build for the phone in your pocket.</b> Your office is a truck cab, a counter, a job site. Everything we ship works one-handed on a phone first — in English and Español.</p>
      <p><b>We use AI where it erases busywork.</b> Scanning receipts, drafting summaries, flagging follow-ups — not another chatbot between you and your work.</p>
      <p><b>Together, they're one system.</b> Start a business with Initor. Find customers with HuntCustomer and bring them through the door with LocalSave. Find workers with OnSMS, run the crew with Ponchi, and run the money with Deskomigo. Each app hands off to the next — an operating system for small business.</p>
      <p class="legal-note">ZET8 is operated by Optima Buildsolutions LLC · Houston, Texas</p>
    </div>
  </div>
</section>
<section class="family" style="padding-top:0">
  <div class="wrap">
    <h2 class="reveal">The ZET8 family</h2>
    <div class="mini-cards">@@MINIS@@</div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap reveal">
    <h2>Want to talk?</h2>
    <p>Questions, demos, partnerships — write to us and a person answers within one business day.</p>
    <a href="/contact/" class="btn btn-primary">Contact us <span class="arrow">→</span></a>
  </div>
</section>
"""

CONTACT = """
<section class="page-hero" style="padding-bottom:0">
  <div class="wrap">
    <div class="eyebrow mono reveal"><span class="dot" style="background:var(--blue)"></span>Contact us</div>
    <h1 class="reveal d1">Talk to a person.</h1>
    <p class="lead reveal d2">Not sure which app fits your business, want a demo, or need help getting set up? Write to us — we reply within one business day.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <div class="cinfo">
          <div class="row"><div class="ico">✉</div><div><b>hello@zet8.com</b><span>Reply within 1 business day</span></div></div>
          <div class="row"><div class="ico">◎</div><div><b>Houston, Texas</b><span>Remote-first · EN &amp; ES</span></div></div>
        </div>
      </div>
      <div class="reveal d1">
        <div class="form">
          <form id="quoteForm">
            <div class="field"><label for="name">Name</label><input type="text" id="name" required placeholder="Jane Smith"></div>
            <div class="two">
              <div class="field"><label for="biz">Company</label><input type="text" id="biz" placeholder="Acme Inc."></div>
              <div class="field"><label for="email">Email</label><input type="email" id="email" required placeholder="jane@company.com"></div>
            </div>
            <div class="field"><label for="need">What you need</label>
              <select id="need">
                <option>Ponchi — workforce management</option>
                <option>Deskomigo — back office app</option>
                <option>HuntCustomer — sales CRM</option>
                <option>LocalSave — local deals</option>
                <option>OnSMS — on-demand hiring</option>
                <option>Initor — business launch</option>
                <option>Not sure — need advice</option>
              </select>
            </div>
            <div class="field"><label for="msg">Tell us about it</label><textarea id="msg" placeholder="What problem are you solving? Who'll use it? Any deadlines?"></textarea></div>
            <button type="submit" class="btn btn-primary">Send <span class="arrow">→</span></button>
          </form>
          <div class="form-success" id="formSuccess">
            <div class="check">✓</div><h3>Message ready.</h3>
            <p>Your email app should open with everything filled in. Hit send — we'll reply within one business day.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

NOTFOUND = """
<section class="page-hero" style="text-align:center;padding-bottom:120px">
  <div class="wrap">
    <div class="eyebrow mono" style="justify-content:center"><span class="dot" style="background:var(--red)"></span>404</div>
    <h1>This page doesn't exist.</h1>
    <p class="lead" style="margin:16px auto 30px">The link may be old or mistyped. Everything we make is one click away.</p>
    <a href="/" class="btn btn-primary">Back to zet8.com <span class="arrow">→</span></a>
  </div>
</section>
"""


# ---------------------------------------------------------------- legal pages
# Source of truth: Desktop/Zet8/tipshare/legal/*.md (attorney-reviewed copies are
# dropped into legal/ here). Editorial markers ("DRAFT" blockquotes, [ATTORNEY]
# flags) stay in the source and are stripped from the published page.

LEGAL_PAGES = [
    {"slug": "tipshare/privacy", "file": "tipshare-privacy.md", "hue": "yellow",
     "title": "TipShare by Ponchi — Privacy Policy | ZET8",
     "desc": "How TipShare by Ponchi collects, uses, and protects merchant and employee data when installed from the Clover App Market."},
    {"slug": "tipshare/terms", "file": "tipshare-terms.md", "hue": "yellow",
     "title": "TipShare by Ponchi — Merchant Terms of Service | ZET8",
     "desc": "The terms under which merchants use TipShare by Ponchi from the Clover App Market."},
]

LEGAL_CSS = """
<style>
  .legal{max-width:760px}
  .legal h1{font-size:clamp(30px,4.6vw,44px);margin-bottom:8px}
  .legal .meta{color:var(--muted);font-family:var(--mono);font-size:13px;margin-bottom:30px}
  .legal h2{font-size:22px;margin:38px 0 10px;color:var(--cream)}
  .legal h3{font-size:17px;margin:24px 0 8px;color:var(--cream)}
  .legal p{margin:0 0 14px;color:var(--text-2)}
  .legal ul{margin:0 0 16px 22px;color:var(--text-2)}
  .legal li{margin:6px 0}
  .legal b{color:var(--text)}
  .legal a{color:var(--yellow);text-decoration:underline;text-underline-offset:3px}
  .legal table{border-collapse:collapse;width:100%;margin:6px 0 18px;font-size:15px}
  .legal th,.legal td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--text-2)}
  .legal th{color:var(--muted);font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
  .legal .box{border:1px solid var(--line-2);background:var(--bg-2);border-radius:var(--radius);padding:14px 18px;margin:0 0 18px}
</style>
"""


def _md_inline(s):
    import html as _h
    import re as _r
    s = _h.escape(s, quote=False)
    s = _r.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = _r.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = _r.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = _r.sub(r"(?<![\"'>=])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', s)
    s = _r.sub(r"(?<![\w@/])([\w.+-]+@[\w-]+\.[\w.-]+)", r'<a href="mailto:\1">\1</a>', s)
    return s


def md_to_html(md):
    """Tiny Markdown subset: #/##/### headings, paragraphs, - lists, | tables |,
    > blockquotes, **bold**, links. Enough for the legal documents, no dependency."""
    import re as _r
    out, para, lst, table, quote = [], [], [], [], []

    def flush():
        nonlocal para, lst, table, quote
        if para:
            out.append("<p>%s</p>" % _md_inline(" ".join(para)))
            para = []
        if lst:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _md_inline(x) for x in lst))
            lst = []
        if table:
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table
                    if not _r.match(r"^\s*\|?\s*-{2,}", r)]
            if rows:
                head = "".join("<th>%s</th>" % _md_inline(c) for c in rows[0])
                body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _md_inline(c) for c in r) for r in rows[1:])
                out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, body))
            table = []
        if quote:
            text = " ".join(quote)
            if "DRAFT" not in text:   # editorial notes never reach the published page
                out.append('<div class="box">%s</div>' % _md_inline(text))
            quote = []

    for raw in md.splitlines():
        line = raw.rstrip()
        line = _r.sub(r"\s*\*\*\[ATTORNEY[^\]]*\]\*\*", "", line)
        if not line.strip():
            flush()
            continue
        if line.startswith("|"):
            if para or lst or quote:
                flush()
            table.append(line)
            continue
        if table:
            flush()
        m = _r.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, _md_inline(m.group(2)), lvl))
            continue
        if line.startswith(">"):
            if para or lst:
                flush()
            quote.append(line.lstrip("> ").strip())
            continue
        if quote:
            flush()
        if _r.match(r"^\s*-\s+", line):
            if para:
                flush()
            lst.append(_r.sub(r"^\s*-\s+", "", line))
            continue
        if lst and line.startswith("  "):
            lst[-1] += " " + line.strip()
            continue
        if lst:
            flush()
        para.append(line.strip())
    flush()
    return "\n".join(out)


def legal_content(spec, md):
    import re as _r
    body = md_to_html(md)
    body = _r.sub(r"^<h1>.*?</h1>\n?", "", body, count=1)       # title rendered in the hero
    body = body.replace("<p><b>Effective date:</b>", '<p class="meta"><b>Effective date:</b>')
    return LEGAL_CSS + """
<section class="page-hero" style="padding-bottom:0">
  <div class="wrap legal">
    <div class="eyebrow mono"><span class="dot" style="background:var(--%s)"></span>TipShare by Ponchi</div>
    <h1>%s</h1>
  </div>
</section>
<section style="padding-top:18px">
  <div class="wrap legal">
%s
    <p class="legal-note" style="margin-top:36px">TipShare by Ponchi is operated by Optima BuildSolutions LLC · Cypress, Texas · <a href="mailto:contact@ponchi.app">contact@ponchi.app</a> · <a href="/tipshare/privacy/">Privacy Policy</a> · <a href="/tipshare/terms/">Merchant Terms</a></p>
  </div>
</section>
""" % (spec["hue"], spec["title"].split(" | ")[0].split(" — ", 1)[1], body)


def main():
    import hashlib
    with open(os.path.join(HERE, "logo-wide-transparent-clean.png"), "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("ascii")
    with open(os.path.join(HERE, "assets", "scene.js"), encoding="utf-8") as f:
        scene_src = f.read()
    scene_v = hashlib.md5(scene_src.encode("utf-8")).hexdigest()[:8]

    def write(rel, html):
        path = os.path.join(HERE, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        io.open(path, "w", encoding="utf-8").write(html)
        print("wrote", rel, "(%d bytes)" % len(html))

    # home (script URL carries a content hash so deploys bust browser caches)
    home = page("ZET8 — Tech Solutions for Businesses",
                "ZET8 is an operating system for small business: start it with Initor, win customers with HuntCustomer and LocalSave, staff it with OnSMS and Ponchi, and run the money with Deskomigo.",
                "/", home_content(logo_b64), logo_b64)
    home = home.replace('<script defer src="/assets/scene.js"></script>',
                        '<script defer src="/assets/scene.js?v=%s"></script>' % scene_v)
    write("index.html", home)

    # product pages
    for p in PRODUCTS:
        title = "%s — %s | ZET8" % (p["name"], p["tagline"].rstrip("."))
        desc = p["card"] + " " + p["pricing"] + "."
        write("%s/index.html" % p["slug"],
              page(title, desc, "/%s/" % p["slug"], product_content(p), logo_b64))

    # legacy redirect: /crm/ moved when the product rebranded to HuntCustomer
    write("crm/index.html",
          '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
          '<meta http-equiv="refresh" content="0; url=/huntcustomer/">'
          '<link rel="canonical" href="https://zet8.com/huntcustomer/">'
          '<title>HuntCustomer | ZET8</title></head>'
          '<body><p><a href="/huntcustomer/">This page moved to zet8.com/huntcustomer/</a></p></body></html>\n')

    # about
    minis = "".join('<a class="mini hue-%s" href="/%s/"><b>%s</b><span>%s</span></a>'
                    % (q["hue"], q["slug"], q["name"], q["cat"]) for q in PRODUCTS)
    write("about/index.html",
          page("About Us | ZET8",
               "ZET8 is a Houston-based software company making finished, ready-to-use apps for small businesses.",
               "/about/", ABOUT.replace("@@MINIS@@", minis), logo_b64, current="about"))

    # contact
    write("contact/index.html",
          page("Contact Us | ZET8",
               "Questions, demos, or help choosing the right ZET8 app? Write to us — a person answers within one business day.",
               "/contact/", CONTACT, logo_b64, extra_js=FORM_JS))

    # 404
    write("404.html",
          page("Page not found | ZET8", "This page doesn't exist.", "/404.html", NOTFOUND, logo_b64))

    # legal pages (TipShare by Ponchi - Clover App Market listing requirement)
    for spec in LEGAL_PAGES:
        with open(os.path.join(HERE, "legal", spec["file"]), encoding="utf-8") as f:
            md = f.read()
        write("%s/index.html" % spec["slug"],
              page(spec["title"], spec["desc"], "/%s/" % spec["slug"], legal_content(spec, md), logo_b64))

    # sitemap
    urls = (["/"] + ["/%s/" % p["slug"] for p in PRODUCTS] + ["/about/", "/contact/"]
            + ["/%s/" % s["slug"] for s in LEGAL_PAGES])
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join("  <url><loc>%s%s</loc><changefreq>weekly</changefreq></url>\n" % (SITE, u) for u in urls)
    sm += "</urlset>\n"
    write("sitemap.xml", sm)

    # artifact preview: home page with absolute links so navigation works from the
    # preview, and the 3D script inlined (the artifact CSP blocks external scripts)
    preview = home.replace('<script defer src="/assets/scene.js?v=%s"></script>' % scene_v,
                           "<script>\n" + scene_src + "\n</script>")
    write("artifact-preview.html", preview.replace('href="/', 'href="%s/' % SITE).replace('href="%s/#' % SITE, 'href="#'))


if __name__ == "__main__":
    main()
