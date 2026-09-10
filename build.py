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
        "tagline": "Need a worker today? Text the job, get offers, pick one.",
        "card": "On-demand hiring by text — post any job, get sealed price offers from workers nearby, and pick one. Same day.",
        "about": "On-demand hiring by text. Need a worker for one task or a full day? Describe the job in a single text and qualified workers nearby reply with their price — you compare the offers and pick one, often the same day. And if you want extra income on your free time, reply to jobs near you, set your own price, and keep 100%. No app on either side.",
        "features": [
            ("Text the job", "Describe what you need in one message. Workers nearby are notified in minutes."),
            ("Get sealed offers", "Workers bid blind with their price. Compare real offers side by side and pick."),
            ("No app required", "Everything runs over plain SMS — no downloads or sign-up on either side."),
            ("Same-day matching", "Urgent staffing and shift coverage typically filled the same day."),
            ("Workers keep 100%", "Pay your worker directly. No markup on wages, no cut taken."),
            ("English + Español", "Fully bilingual for employers and workers alike."),
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
    <div class="foot-bottom"><span>© 2026 ZET8 · all rights reserved</span><span>Cypress, TX · zet8.com</span></div>
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
  "address": {"@type": "PostalAddress","streetAddress": "12320 Barker Cypress Rd, Ste 600 #199","addressLocality": "Cypress","addressRegion": "TX","postalCode": "77429","addressCountry": "US"},
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


# ---------------------------------------------------- OnSMS bespoke landing page
# OnSMS gets its own rich, self-explaining landing page (dual-audience: businesses
# who need a task done + workers who want extra income). All other products use
# the shared product_content() template above. Scoped CSS uses the `.os-` prefix.
def onsms_content(p):
    minis = "".join("""
      <a class="mini hue-%s" href="/%s/"><b>%s</b><span>%s</span></a>""" % (
        q["hue"], q["slug"], q["name"], q["cat"]) for q in PRODUCTS if q["slug"] != "onsms")
    html = r"""
<style>
  .os h1,.os h2,.os h3,.os h4{font-family:var(--disp);color:var(--cream);letter-spacing:-.03em;line-height:1.06}
  .os .hl{color:var(--green)}
  .os-eyebrow{display:inline-flex;align-items:center;gap:9px;font-family:var(--mono);font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--green);border:1px solid var(--line-2);padding:7px 14px;border-radius:100px;margin-bottom:26px}
  .os-dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(60,179,113,.16)}
  /* HERO */
  .os-hero{padding:132px 0 44px}
  .os-hero-grid{display:grid;grid-template-columns:1.04fr .96fr;gap:56px;align-items:center}
  .os-hero-copy h1{font-size:clamp(34px,5.1vw,60px);margin-bottom:22px}
  .os-lead{font-size:1.13rem;color:var(--text-2);max-width:46ch;margin-bottom:30px;line-height:1.6}
  .os-cta{display:flex;gap:13px;flex-wrap:wrap;margin-bottom:22px}
  .os-btn-outline{background:transparent;color:var(--cream);border:1.5px solid var(--line-2)}
  .os-btn-outline:hover{border-color:var(--green);color:var(--green);transform:translateY(-2px)}
  .os-trust{display:flex;gap:10px;flex-wrap:wrap;font-size:.86rem;color:var(--muted);align-items:center}
  .os-trust b{color:var(--text-2);font-weight:500}
  /* PHONE MOCKUP */
  .os-hero-visual{display:flex;justify-content:center}
  .os-phone{width:335px;max-width:100%;background:var(--bg-2);border:1px solid var(--line-2);border-radius:36px;padding:15px 14px 20px;box-shadow:0 44px 100px -34px rgba(0,0,0,.92),0 0 0 1px rgba(60,179,113,.07);position:relative}
  .os-phone::before{content:"";position:absolute;top:20px;left:50%;transform:translateX(-50%);width:52px;height:5px;border-radius:5px;background:var(--line-2)}
  .os-phone-top{text-align:center;color:var(--muted);font-family:var(--mono);font-size:.64rem;letter-spacing:.16em;text-transform:uppercase;padding:18px 0 12px;border-bottom:1px solid var(--line);margin-bottom:15px}
  .os-phone-top b{color:var(--green)}
  .os-thread{display:flex;flex-direction:column;gap:10px;padding:2px 4px}
  .os-msg{max-width:84%;padding:11px 14px;border-radius:17px;font-size:.89rem;line-height:1.42}
  .os-msg.out{align-self:flex-end;background:var(--green);color:#04140c;border-bottom-right-radius:5px;font-weight:500}
  .os-msg.small{padding:9px 15px;font-weight:600}
  .os-sys{align-self:center;font-size:.7rem;color:var(--muted);font-family:var(--mono);letter-spacing:.03em;text-align:center;padding:2px 0}
  .os-sys.ok{color:var(--green)}
  .os-offer{align-self:flex-start;display:flex;align-items:center;gap:11px;background:var(--bg-3);border:1px solid var(--line-2);border-radius:15px;padding:9px 13px;width:90%;box-shadow:0 6px 18px -12px rgba(0,0,0,.7)}
  .os-av{width:35px;height:35px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--disp);font-weight:700;font-size:.92rem;color:#04140c;flex:none}
  .os-offer .nm b{font-size:.88rem;color:var(--cream);display:block;line-height:1.2}
  .os-offer .nm small{font-size:.7rem;color:var(--muted)}
  .os-price{margin-left:auto;font-family:var(--disp);font-weight:700;font-size:1.08rem;color:var(--green)}
  /* SECTIONS */
  .os-sec{padding:74px 0;border-top:1px solid var(--line)}
  .os-sec-head{text-align:center;max-width:640px;margin:0 auto 48px}
  .os-kicker{font-family:var(--mono);font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--green);margin-bottom:14px}
  .os-sec-head h2{font-size:clamp(28px,3.7vw,42px);margin-bottom:14px}
  .os-sec-head p{color:var(--text-2);font-size:1.06rem}
  /* STEPS */
  .os-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
  .os-step{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--radius-lg);padding:34px 30px}
  .os-num{font-family:var(--disp);font-weight:700;font-size:1rem;width:42px;height:42px;border-radius:50%;background:rgba(60,179,113,.12);color:var(--green);display:flex;align-items:center;justify-content:center;margin-bottom:20px;border:1px solid rgba(60,179,113,.32)}
  .os-step h3{font-size:1.32rem;margin-bottom:10px}
  .os-step p{color:var(--text-2);font-size:.96rem}
  /* SPLIT (two audiences) */
  .os-split{display:grid;grid-template-columns:1fr 1fr;gap:24px}
  .os-card2{border:1px solid var(--line-2);border-radius:var(--radius-lg);padding:42px 36px;background:linear-gradient(180deg,var(--bg-2),var(--bg))}
  .os-card2.worker{border-color:rgba(60,179,113,.4);background:linear-gradient(180deg,rgba(60,179,113,.06),var(--bg))}
  .os-tag2{font-family:var(--mono);font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--green);margin-bottom:16px;display:block}
  .os-card2 h3{font-size:1.72rem;margin-bottom:14px}
  .os-card2>p{color:var(--text-2);margin-bottom:22px}
  .os-list{list-style:none;display:flex;flex-direction:column;gap:12px;margin-bottom:30px}
  .os-list li{display:flex;gap:11px;align-items:flex-start;color:var(--text-2);font-size:.97rem}
  .os-list li::before{content:"\2713";color:var(--green);font-weight:700;flex:none}
  /* CHIPS */
  .os-chips{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;max-width:840px;margin:0 auto}
  .os-chip{display:inline-flex;align-items:center;gap:9px;background:var(--bg-2);border:1px solid var(--line-2);border-radius:100px;padding:12px 20px;font-size:.95rem;color:var(--text);transition:.2s}
  .os-chip:hover{border-color:var(--green);color:var(--cream);transform:translateY(-2px)}
  .os-chip .em{font-size:1.06rem}
  /* WHY */
  .os-why{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
  .os-why-item{padding:30px 28px;border:1px solid var(--line);border-radius:var(--radius);background:var(--bg-2)}
  .os-ic{font-size:1.5rem;margin-bottom:14px}
  .os-why-item h4{font-size:1.12rem;margin-bottom:8px}
  .os-why-item p{color:var(--text-2);font-size:.92rem}
  /* FAQ */
  .os-faq{max-width:770px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
  .os-q{border:1px solid var(--line);border-radius:15px;background:var(--bg-2);padding:23px 27px}
  .os-q h4{font-size:1.08rem;margin-bottom:8px}
  .os-q p{color:var(--text-2);font-size:.95rem}
  /* FINAL */
  .os-final{text-align:center;padding:96px 0;border-top:1px solid var(--line);background:radial-gradient(ellipse at 50% 0%,rgba(60,179,113,.1),transparent 62%)}
  .os-final h2{font-size:clamp(30px,4.6vw,52px);margin-bottom:18px}
  .os-final>.wrap>p{color:var(--text-2);font-size:1.12rem;margin:0 auto 32px;max-width:52ch}
  .os-final .os-cta{justify-content:center}
  .os-note{margin-top:24px;font-family:var(--mono);font-size:.73rem;letter-spacing:.05em;color:var(--muted)}
  @media(max-width:900px){
    .os-hero-grid{grid-template-columns:1fr;gap:42px}
    .os-hero{padding:112px 0 24px}
    .os-lead{max-width:none}
    .os-steps,.os-why{grid-template-columns:1fr}
    .os-split{grid-template-columns:1fr}
  }
</style>
<div class="hue-green os">

<section class="os-hero">
  <div class="wrap os-hero-grid">
    <div class="os-hero-copy">
      <div class="os-eyebrow reveal"><span class="os-dot"></span>On-demand hiring by text &middot; Texas</div>
      <h1 class="reveal d1">Need a worker <span class="hl">today?</span><br>Text the job. Get offers. Pick one.</h1>
      <p class="os-lead reveal d2">Whether it&rsquo;s one quick task or a full day of help, describe what you need in a single text. Qualified workers nearby reply with their price &mdash; you compare the offers and pick the one you want. Often matched the same day. No app, no agency, no markup on wages.</p>
      <div class="os-cta reveal d3">
        <a class="btn btn-hue" href="@@URL@@" target="_blank" rel="noopener">Post a job &mdash; get prices <span class="arrow">&rarr;</span></a>
        <a class="btn os-btn-outline" href="@@URL@@" target="_blank" rel="noopener">Earn on your free time</a>
      </div>
      <div class="os-trust reveal d4"><b>No app to download</b> &middot; <b>Workers keep 100%</b> &middot; <b>English &amp; Espa&ntilde;ol</b></div>
    </div>
    <div class="os-hero-visual reveal d2">
      <div class="os-phone">
        <div class="os-phone-top">on<b>sms</b> &middot; today 9:04 AM</div>
        <div class="os-thread">
          <div class="os-msg out">Need 2 people to help move a couch &amp; boxes. Sat 10 AM, Katy TX. ~2 hrs.</div>
          <div class="os-sys">&#10003; Sent to 14 available workers near you</div>
          <div class="os-offer"><span class="os-av" style="background:#F4C82D">M</span><span class="nm"><b>Marcus D.</b><small>&#9733; 4.9 &middot; 63 jobs</small></span><span class="os-price">$50</span></div>
          <div class="os-offer"><span class="os-av" style="background:#3CB371">A</span><span class="nm"><b>Ana R.</b><small>&#9733; 5.0 &middot; 41 jobs</small></span><span class="os-price">$40</span></div>
          <div class="os-offer"><span class="os-av" style="background:#5468E8">T</span><span class="nm"><b>Tobias K.</b><small>&#9733; 4.8 &middot; 28 jobs</small></span><span class="os-price">$55</span></div>
          <div class="os-msg out small">Pick Ana &#128077;</div>
          <div class="os-sys ok">&#10003; Ana is confirmed for Sat 10 AM. She&rsquo;ll text when she&rsquo;s on the way.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="os-sec">
  <div class="wrap">
    <div class="os-sec-head reveal">
      <div class="os-kicker">How it works</div>
      <h2>Three texts from &ldquo;I need help&rdquo; to &ldquo;done.&rdquo;</h2>
      <p>No forms, no phone tag, no waiting on an agency to call you back.</p>
    </div>
    <div class="os-steps">
      <div class="os-step reveal"><div class="os-num">1</div><h3>Text your job</h3><p>Describe what you need, where, and when &mdash; in one message. That&rsquo;s the whole &ldquo;form.&rdquo; We instantly notify available workers nearby.</p></div>
      <div class="os-step reveal"><div class="os-num">2</div><h3>Get sealed offers</h3><p>Workers reply with their name, rating, and price. Offers are sealed &mdash; they bid blind, so you get honest market rates side by side.</p></div>
      <div class="os-step reveal"><div class="os-num">3</div><h3>Pick your worker</h3><p>Choose the offer you like best. Your worker shows up and you pay them directly. First two hires are on us.</p></div>
    </div>
  </div>
</section>

<section class="os-sec">
  <div class="wrap">
    <div class="os-split">
      <div class="os-card2 reveal">
        <span class="os-tag2">For businesses &amp; homeowners</span>
        <h3>Get a price for your task.</h3>
        <p>A short task or a full day of help &mdash; post it once and let qualified workers come to you with real prices. You stay in control the whole way.</p>
        <ul class="os-list">
          <li>Same-day matching for urgent jobs and shift coverage</li>
          <li>Compare real offers and pick &mdash; never a take-it-or-leave-it quote</li>
          <li>No agency fees and no markup on what workers charge</li>
          <li>Every worker is rated by past customers</li>
        </ul>
        <a class="btn btn-hue" href="@@URL@@" target="_blank" rel="noopener">Post a job <span class="arrow">&rarr;</span></a>
      </div>
      <div class="os-card2 worker reveal">
        <span class="os-tag2">For workers</span>
        <h3>Want extra income on your free time?</h3>
        <p>Turn a free afternoon into cash. Get a text when there&rsquo;s a job near you, reply with your price, and work only when you want to.</p>
        <ul class="os-list">
          <li>No app to install &mdash; just reply to a text message</li>
          <li>Set your own price on every single job</li>
          <li>Keep 100% of what you earn &mdash; we never touch your pay</li>
          <li>Pick up as much or as little work as you like</li>
        </ul>
        <a class="btn btn-hue" href="@@URL@@" target="_blank" rel="noopener">Start earning <span class="arrow">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>

<section class="os-sec">
  <div class="wrap">
    <div class="os-sec-head reveal">
      <div class="os-kicker">What people hire for</div>
      <h2>If it&rsquo;s a job someone can show up and do, post it.</h2>
    </div>
    <div class="os-chips reveal">
      <span class="os-chip"><span class="em">&#128230;</span>Moving &amp; loading</span>
      <span class="os-chip"><span class="em">&#129529;</span>Cleaning</span>
      <span class="os-chip"><span class="em">&#127794;</span>Yard &amp; landscaping</span>
      <span class="os-chip"><span class="em">&#128295;</span>Handyman help</span>
      <span class="os-chip"><span class="em">&#127959;&#65039;</span>Construction labor</span>
      <span class="os-chip"><span class="em">&#128666;</span>Delivery &amp; errands</span>
      <span class="os-chip"><span class="em">&#127869;&#65039;</span>Event &amp; restaurant</span>
      <span class="os-chip"><span class="em">&#127981;</span>Warehouse</span>
      <span class="os-chip"><span class="em">&#128296;</span>Painting</span>
      <span class="os-chip"><span class="em">&#9201;&#65039;</span>Shift coverage</span>
    </div>
  </div>
</section>

<section class="os-sec">
  <div class="wrap">
    <div class="os-sec-head reveal">
      <div class="os-kicker">Why onsms</div>
      <h2>Hiring stripped down to a text message.</h2>
    </div>
    <div class="os-why">
      <div class="os-why-item reveal"><div class="os-ic">&#128274;</div><h4>Sealed offers</h4><p>Workers bid without seeing each other, so you get honest market prices &mdash; not padded quotes.</p></div>
      <div class="os-why-item reveal"><div class="os-ic">&#128241;</div><h4>No app needed</h4><p>Everything happens over plain SMS. Nothing to download, install, or log into &mdash; on either side.</p></div>
      <div class="os-why-item reveal"><div class="os-ic">&#9889;</div><h4>Same-day</h4><p>Post in the morning, get help by the afternoon. Built for urgent needs and last-minute gaps.</p></div>
      <div class="os-why-item reveal"><div class="os-ic">&#128181;</div><h4>Workers keep 100%</h4><p>You pay your worker directly. onsms never takes a cut of anyone&rsquo;s wages.</p></div>
      <div class="os-why-item reveal"><div class="os-ic">&#11088;</div><h4>Rated &amp; real</h4><p>Every worker carries a star rating and job history from real past customers.</p></div>
      <div class="os-why-item reveal"><div class="os-ic">&#127760;</div><h4>Bilingual</h4><p>Fully in English and Espa&ntilde;ol, for employers and workers alike.</p></div>
    </div>
  </div>
</section>

<section class="os-sec">
  <div class="wrap">
    <div class="os-sec-head reveal">
      <div class="os-kicker">Questions</div>
      <h2>Good to know</h2>
    </div>
    <div class="os-faq">
      <div class="os-q reveal"><h4>What does it cost?</h4><p>Your first two hires are free. After that it&rsquo;s a flat $15 per confirmed hire &mdash; no subscription. Workers never pay anything.</p></div>
      <div class="os-q reveal"><h4>Do workers need to download an app?</h4><p>No. Workers get a plain text message and reply with their price. That&rsquo;s the whole thing &mdash; it works on any phone.</p></div>
      <div class="os-q reveal"><h4>How do I pay the worker?</h4><p>Directly &mdash; cash, Venmo, Zelle, whatever you both agree on. onsms matches you and steps out of the money.</p></div>
      <div class="os-q reveal"><h4>What kind of jobs can I post?</h4><p>Anything hands-on and legal &mdash; from a two-hour moving job to several days of shift coverage. If someone can show up and do it, you can post it.</p></div>
      <div class="os-q reveal"><h4>Where is onsms available?</h4><p>Launching across Texas first &mdash; Houston, Katy, Cypress and nearby &mdash; and expanding from there. Post a job and we&rsquo;ll tell you what&rsquo;s available near you.</p></div>
    </div>
  </div>
</section>

<section class="os-final">
  <div class="wrap">
    <h2 class="reveal">Need something done today?</h2>
    <p class="reveal">Post your job in one text and start getting offers from workers near you within minutes.</p>
    <div class="os-cta reveal">
      <a class="btn btn-hue" href="@@URL@@" target="_blank" rel="noopener">Post a job <span class="arrow">&rarr;</span></a>
      <a class="btn os-btn-outline" href="@@URL@@" target="_blank" rel="noopener">Work with onsms</a>
    </div>
    <div class="os-note reveal">First 2 hires free &middot; then $15 per confirmed hire &middot; workers always free</div>
  </div>
</section>

<section class="family">
  <div class="wrap">
    <h2 class="reveal">More from ZET8</h2>
    <div class="mini-cards">@@MINIS@@</div>
  </div>
</section>
</div>
"""
    return (html.replace("@@MINIS@@", minis)
                .replace("@@URL@@", p["url"])
                .replace("@@DOMAIN@@", p["domain"]))


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
      <p class="legal-note">ZET8 is operated by Optima Buildsolutions LLC · 12320 Barker Cypress Rd, Ste 600 #199, Cypress, TX 77429</p>
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
          <div class="row"><div class="ico">◎</div><div><b>12320 Barker Cypress Rd, Ste 600 #199, Cypress, TX 77429</b><span>Remote-first · EN &amp; ES</span></div></div>
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
    <p class="legal-note" style="margin-top:36px">TipShare by Ponchi is operated by Optima BuildSolutions LLC · 12320 Barker Cypress Rd, Ste 600 #199, Cypress, TX 77429 · <a href="mailto:contact@ponchi.app">contact@ponchi.app</a> · <a href="/tipshare/privacy/">Privacy Policy</a> · <a href="/tipshare/terms/">Merchant Terms</a></p>
  </div>
</section>
""" % (spec["hue"], spec["title"].split(" | ")[0].split(" — ", 1)[1], body)


# ------------------------------------------------- TipShare by Ponchi landing page
# The "website" link on the Clover App Market listing. Screenshots and art come
# from Desktop/Zet8/tipshare/listing (web-sized copies live in tipshare/img/).
# Scoped CSS uses the `.ts-` prefix; colours follow the TipShare logo (navy /
# yellow / light blue) inside the site's dark theme.

TIPSHARE_CSS = """
<style>
  .ts-hero{padding:72px 0 40px}
  .ts-hero .wrap{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:44px;align-items:center}
  .ts-hero h1{font-size:clamp(34px,5vw,56px);line-height:1.05;margin:10px 0 14px}
  .ts-hero h1 em{font-style:normal;color:#F0B808}
  .ts-hero .lead{font-size:19px;color:var(--text-2);max-width:56ch;margin:0 0 22px}
  .ts-hero .logo{width:300px;height:300px;border-radius:28px;box-shadow:0 30px 80px -30px rgba(0,0,0,.7)}
  .ts-badge{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line-2);background:var(--bg-2);border-radius:999px;padding:6px 14px;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#88C8D8}
  .ts-badge i{width:8px;height:8px;border-radius:50%;background:#F0B808;display:inline-block}
  .ts-note{color:var(--muted);font-size:14px;margin-top:14px}
  .ts-shot{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#0B1F3A;box-shadow:0 30px 80px -40px rgba(0,0,0,.8)}
  .ts-shot img{display:block;width:100%;height:auto}
  .ts-shots{display:grid;grid-template-columns:1fr;gap:28px;margin-top:8px}
  .ts-row{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:32px;align-items:center}
  .ts-row.flip{grid-template-columns:minmax(0,1fr) minmax(0,1.4fr)}
  .ts-row h3{font-size:24px;margin:0 0 10px}
  .ts-row p{color:var(--text-2);margin:0 0 10px}
  .ts-row ul{margin:0 0 0 20px;color:var(--text-2)}
  .ts-row li{margin:5px 0}
  .ts-fits{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
  .ts-fit{border:1px solid var(--line);background:var(--bg-2);border-radius:var(--radius);padding:16px 18px}
  .ts-fit b{display:block;color:var(--cream);margin-bottom:4px}
  .ts-fit span{color:var(--text-2);font-size:14px}
  .ts-price{border:1px solid #F0B808;border-radius:var(--radius);padding:26px 28px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:20px;align-items:center;background:linear-gradient(135deg,rgba(240,184,8,.08),rgba(136,200,216,.06))}
  .ts-price .amt{font-size:40px;font-weight:800;color:var(--cream);line-height:1}
  .ts-price .amt small{font-size:16px;color:var(--text-2);font-weight:500;margin-left:6px}
  .ts-price p{margin:8px 0 0;color:var(--text-2)}
  .ts-phone{max-width:300px;margin:0 auto}
  .ts-faq{display:grid;gap:0}
  .ts-faq details{border-bottom:1px solid var(--line);padding:14px 0}
  .ts-faq summary{cursor:pointer;font-weight:600;color:var(--cream);list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center}
  .ts-faq summary::-webkit-details-marker{display:none}
  .ts-faq summary::after{content:'+';color:#F0B808;font-size:20px;line-height:1}
  .ts-faq details[open] summary::after{content:'2'}
  .ts-faq p{color:var(--text-2);margin:10px 0 0;max-width:70ch}
  .ts-support{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:8px}
  .ts-support div{border:1px solid var(--line);background:var(--bg-2);border-radius:var(--radius);padding:16px 18px}
  .ts-support b{display:block;color:var(--cream);margin-bottom:4px}
  .ts-support a{color:#88C8D8}
  .ts-legal{color:var(--muted);font-size:13px;margin-top:28px}
  .ts-legal a{color:#88C8D8}
  @media(max-width:860px){.ts-hero .wrap,.ts-row,.ts-row.flip{grid-template-columns:1fr}.ts-hero .logo{width:200px;height:200px;margin:0 auto}.ts-price{grid-template-columns:1fr}}
</style>
"""

# Clover requires the support website to carry FAQs, privacy policy, terms, a support
# email and a phone number. Set this to the number TipShare support should ring on;
# empty leaves the phone card off the page (and prints a warning at build time).
TIPSHARE_PHONE = "(346) 332-6440"

TIPSHARE_FAQ = [
    ("Do I need Ponchi to use TipShare?",
     "No. TipShare works on its own using hours from the Clover time clock, or from a punch report you "
     "upload. Ponchi is our time-clock app: if you use it, hours land in every tip period automatically, "
     "and you can start a 14-day trial from inside TipShare."),
    ("How do the tips get from Clover into TipShare?",
     "TipShare reads your sales, card tips and gratuities from Clover for the period you pick, and "
     "attributes each sale to the person and shift that rang it. Nothing is written back to Clover, and "
     "no payment or card data is stored."),
    ("Can it handle our house rules?",
     "Yes. Tip-outs can be a percent of sales or of tips, from any role to a pool or to support staff; "
     "pools split by hours with optional weights; rules can differ by day and by shift. Start from a "
     "standard setup for your kind of business, paste the tip sheet you use today, or answer a short "
     "guided interview. Every path previews on a real period before anything changes."),
    ("What about cash tips?",
     "Your choice: not tracked, declared per person per shift (managers or the employees themselves), or "
     "one cash jar per shift split with the pool. You also say whether cash is taken home the same night "
     "or paid through payroll, and payroll shows both separately."),
    ("Can employees see their own tips?",
     "Only if you turn it on. Each person then gets a private page, in English or Spanish, showing their "
     "own shifts and totals with a plain-English explanation. Nobody sees anyone else's numbers."),
    ("Does someone need to be at the computer?",
     "No. Owners and managers see today's numbers and the current period on the Clover device, and the "
     "full dashboard opens from the Clover web dashboard. A period can also be pulled automatically every "
     "Monday with an email of anything that needs attention."),
    ("What does it cost?",
     "$29 per month per location with a 30-day free trial, billed through the Clover App Market. Cancel "
     "any time from the App Market; there are no per-device fees."),
    ("Is TipShare telling me what is legal?",
     "No. TipShare calculates exactly what you configure and keeps a record of every change. Tip laws "
     "vary by state, so confirm your practices with a labor attorney or your state labor department."),
    ("What happens to my data if I uninstall?",
     "Your periods stay available while the subscription is active. After an uninstall we delete or "
     "de-identify the data within 90 days, and you can ask for a copy at any time by emailing us."),
]


TIPSHARE_FITS = [
    ("Restaurants", "Servers tip out the bar and support staff; pools split by hours."),
    ("Bars & lounges", "Different rules by night, solo weeknights, Sunday tips-based tip-outs."),
    ("Cafés & counter service", "Card tips and the cash jar in one pool for everyone on the clock."),
    ("Hotels & banquets", "Service charges pooled by hours across servers, captains and bartenders."),
    ("Salons & spas", "Each provider keeps their tips; assistants and front desk as support."),
    ("Your own rules", "Percent of sales or tips, weights, cash declared or jarred, all yours to set."),
]


def tipshare_content():
    fits = "".join('<div class="ts-fit reveal"><b>%s</b><span>%s</span></div>' % f for f in TIPSHARE_FITS)
    faq_html = "".join('<details class="reveal"><summary>%s</summary><p>%s</p></details>' % f
                       for f in TIPSHARE_FAQ)
    digits = "".join(c for c in TIPSHARE_PHONE if c.isdigit())
    phone_html = ('      <div class="reveal d1"><b>Phone</b><a href="tel:+1%s">%s</a><br>'
                  '<span style="color:var(--muted);font-size:13px">Mon-Fri, 9am-6pm Central.</span></div>\n'
                  % (digits, TIPSHARE_PHONE)) if digits else ''
    if not digits:
        print('  ! TIPSHARE_PHONE is empty — the Clover listing needs a support phone number')
    return TIPSHARE_CSS + """
<div class="hue-yellow">
<section class="ts-hero">
  <div class="wrap">
    <div>
      <div class="crumbs reveal"><a href="/">Home</a><span class="sep">/</span><a href="/ponchi/">Ponchi</a><span class="sep">/</span>TipShare</div>
      <span class="ts-badge reveal"><i></i>Clover App Market</span>
      <h1 class="reveal d1">Tip pools and tip-outs,<br>straight from your <em>Clover sales</em>.</h1>
      <p class="lead reveal d2">TipShare pulls every sale, card tip and gratuity from Clover, applies your house rules, and hands you a payroll-ready total for each employee every week. No spreadsheet. No arguments.</p>
      <div class="cta-row reveal d3">
        <a class="btn btn-hue" href="/contact/">Get notified at launch <span class="arrow">→</span></a>
        <a class="btn btn-ghost" href="/ponchi/">See Ponchi</a>
      </div>
      <p class="ts-note reveal d4">Coming to the Clover App Market for U.S. merchants. $29 a month, 30-day free trial, billed through Clover.</p>
    </div>
    <img class="logo reveal d2" src="/tipshare/img/logo.png" alt="TipShare by Ponchi" width="300" height="300">
  </div>
</section>

<section>
  <div class="wrap ts-shots">
    <div class="ts-row">
      <div class="ts-shot reveal"><img src="/tipshare/img/shifts.jpg" alt="Every person and shift: sales, gratuity, card tips, tip-outs, net take-home" loading="lazy"></div>
      <div class="reveal d1"><h3>One click, the whole week</h3>
        <p>Pull the week from Clover and every sale lands on the person and shift that earned it. Morning and night split at your hour; doubles handled; hours from Clover, from Ponchi, or from a punch report.</p>
        <ul><li>Card tips and gratuity counted as tips, service charges included</li><li>Tip-outs as a percent of sales or of tips, to a pool or to support staff</li><li>Cash tips declared per person or counted from the jar</li></ul></div>
    </div>
    <div class="ts-row flip">
      <div class="reveal d1"><h3>Payroll without the argument</h3>
        <p>Finalize the week and export it: PDF, Excel, CSV, or email it to your bookkeeper. Cash already in hand is separated from what goes through payroll.</p>
        <ul><li>"Explain this week" writes a plain-English breakdown for any employee</li><li>Optional private tip page for each employee, showing only their own shifts</li><li>Every change is logged, so last month's payroll is always defensible</li></ul></div>
      <div class="ts-shot reveal"><img src="/tipshare/img/payroll.jpg" alt="Payroll-ready totals per employee with cash in hand and payroll due" loading="lazy"></div>
    </div>
    <div class="ts-row">
      <div class="ts-shot reveal"><img src="/tipshare/img/setup.jpg" alt="Standard setups by business type, import your current tip sheet, or a guided interview" loading="lazy"></div>
      <div class="reveal d1"><h3>Set up in minutes, three ways</h3>
        <p>Pick a standard setup for your kind of business, paste the tip sheet you use today and let the assistant infer your rules, or answer a short guided interview. Every path previews on a real week before you apply it.</p>
        <p>The assistant only writes the rules; every dollar is computed by the same engine, every time.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal"><div class="eyebrow mono"><span class="dot" style="background:#F0B808"></span>Built for</div><h2>Any place that pools or tips out</h2></div>
    <div class="ts-fits">%(fits)s</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="ts-row">
      <div class="reveal"><h3>On the Clover device too</h3>
        <p>Owners and managers see today's live numbers and this week's status right on the Flex, Mini or Station Duo. Employees logged into the device see their own tips, and only if you turn that on.</p>
        <p>Hours come free with <a href="/ponchi/" style="color:#F0B808">Ponchi</a>, our time clock: GPS clock-ins land in every tip week automatically. A 14-day Ponchi trial starts from inside TipShare.</p></div>
      <div class="ts-phone reveal d1"><div class="ts-shot"><img src="/tipshare/img/employee.jpg" alt="An employee's own tip page on a phone" loading="lazy"></div></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="ts-price reveal">
      <div><div class="amt">$29<small>per month, per location</small></div>
        <p>30-day free trial, billed through Clover, cancel any time from the App Market. No per-device fees. TipShare calculates what you configure; tip laws vary by state, so confirm your practices with a labor attorney.</p></div>
      <a class="btn btn-hue" href="/contact/">Get notified at launch <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal"><div class="eyebrow mono"><span class="dot" style="background:#F0B808"></span>Questions</div><h2>Frequently asked</h2></div>
    <div class="ts-faq">%(faq)s</div>
  </div>
</section>

<section id="support">
  <div class="wrap">
    <div class="sec-head reveal"><div class="eyebrow mono"><span class="dot" style="background:#88C8D8"></span>Support</div><h2>Help with TipShare</h2></div>
    <div class="ts-support">
      <div class="reveal"><b>Email</b><a href="mailto:contact@ponchi.app">contact@ponchi.app</a><br><span style="color:var(--muted);font-size:13px">A person answers within one business day.</span></div>
%(phone)s      <div class="reveal d2"><b>Documents</b><a href="/tipshare/privacy/">Privacy Policy</a> · <a href="/tipshare/terms/">Merchant Terms</a></div>
    </div>
    <p class="ts-legal">TipShare by Ponchi is operated by Optima BuildSolutions LLC, 12320 Barker Cypress Rd, Ste 600 #199, Cypress, TX 77429 · <a href="mailto:contact@ponchi.app">contact@ponchi.app</a> · <a href="/tipshare/privacy/">Privacy Policy</a> · <a href="/tipshare/terms/">Merchant Terms</a></p>
  </div>
</section>
</div>
""" % {"fits": fits, "faq": faq_html, "phone": phone_html}


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

    # product pages (OnSMS has its own bespoke landing page; the rest share one)
    for p in PRODUCTS:
        title = "%s — %s | ZET8" % (p["name"], p["tagline"].rstrip("."))
        desc = p["card"] + " " + p["pricing"] + "."
        content = onsms_content(p) if p["slug"] == "onsms" else product_content(p)
        write("%s/index.html" % p["slug"],
              page(title, desc, "/%s/" % p["slug"], content, logo_b64))

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

    # TipShare by Ponchi — the Clover App Market listing's website link
    write("tipshare/index.html",
          page("TipShare by Ponchi — Tip pools and tip-outs from your Clover sales | ZET8",
               "TipShare turns Clover sales, card tips and gratuities into payroll-ready tip totals for every employee, every week. $29/mo, 30-day free trial, on the Clover App Market.",
               "/tipshare/", tipshare_content(), logo_b64))

    # legal pages (TipShare by Ponchi — Clover App Market listing requirement)
    for spec in LEGAL_PAGES:
        with open(os.path.join(HERE, "legal", spec["file"]), encoding="utf-8") as f:
            md = f.read()
        write("%s/index.html" % spec["slug"],
              page(spec["title"], spec["desc"], "/%s/" % spec["slug"], legal_content(spec, md), logo_b64))

    # sitemap
    urls = (["/"] + ["/%s/" % p["slug"] for p in PRODUCTS] + ["/about/", "/contact/", "/tipshare/"]
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
