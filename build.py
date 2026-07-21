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
        "slug": "crm", "name": "Zet8 CRM", "hue": "blue", "cat": "Sales",
        "domain": "crm.zet8.com", "url": "https://crm.zet8.com",
        "tagline": "The CRM that gets out of your way.",
        "card": "Deals, contacts, and follow-ups in one clutter-free workspace for small sales teams.",
        "about": "A streamlined CRM for small sales teams. Deals, contacts, and follow-ups in one clutter-free workspace — no feature bloat, no hidden per-feature costs, no six-week onboarding.",
        "features": [
            ("Visual pipeline", "Drag deals across stages you define. See what's stuck and what's closing."),
            ("One customer record", "Contacts, deals, and every conversation in a single timeline."),
            ("Smart follow-ups", "Your dashboard tells you who to call today, so leads stop going cold."),
            ("Team workspace", "Assign deals, thread conversations, and keep the whole team on the same page."),
            ("No bloat", "Everything included at one price — no per-feature upsells."),
            ("Cancel anytime", "Month-to-month billing. Stay because it works, not because you're locked in."),
        ],
        "pricing": "$14.99/user/mo · 14-day free trial",
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
]

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

  /* HERO (home) */
  .hero{padding:150px 0 90px;position:relative;overflow:hidden;text-align:center}
  .hero::before,.hero::after{content:"";position:absolute;border-radius:50%;filter:blur(80px);opacity:.12;z-index:0;pointer-events:none}
  .hero::before{width:520px;height:520px;background:var(--green);top:-140px;left:-120px}
  .hero::after{width:560px;height:560px;background:var(--blue);bottom:-240px;right:-140px}
  .hero-inner{position:relative;z-index:1}
  .hero-logo{width:min(360px,68vw);height:auto;margin:0 auto 30px;display:block;filter:drop-shadow(0 30px 60px rgba(0,0,0,.55))}
  .hero h1{font-size:clamp(2.1rem,5.5vw,4.2rem);max-width:820px;margin:0 auto}
  .hero .sub{font-size:1.12rem;color:var(--text-2);max-width:580px;margin:24px auto 34px;line-height:1.55}
  .hero-cta{display:flex;gap:13px;flex-wrap:wrap;justify-content:center}
  .hero-meta{margin-top:44px;display:flex;justify-content:center;gap:30px;flex-wrap:wrap;font-family:var(--mono);font-size:.76rem;color:var(--muted);letter-spacing:.06em}
  .hero-meta span{display:flex;align-items:center;gap:8px}
  .hero-meta span::before{content:"";width:8px;height:8px;border-radius:2px;display:inline-block}
  .hero-meta span:nth-child(1)::before{background:var(--green)}
  .hero-meta span:nth-child(2)::before{background:var(--yellow)}
  .hero-meta span:nth-child(3)::before{background:var(--red)}
  .hero-meta span:nth-child(4)::before{background:var(--blue)}

  .reveal{opacity:0;transform:translateY(26px);transition:.8s var(--ease)}
  .reveal.in{opacity:1;transform:none}
  .d1{transition-delay:.06s}.d2{transition-delay:.13s}.d3{transition-delay:.2s}.d4{transition-delay:.27s}

  section{padding:96px 0;position:relative}
  .sec-head{max-width:720px;margin-bottom:44px}
  .sec-head h2{font-size:clamp(1.8rem,4vw,2.9rem);margin:14px 0}
  .sec-head p{color:var(--text-2);font-size:1.05rem;max-width:600px}
  .eyebrow{display:inline-flex;align-items:center;gap:10px}
  .eyebrow .dot{width:9px;height:9px;border-radius:50%;display:inline-block}

  /* PRODUCT CARDS (home) */
  #products{background:var(--bg-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
  .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .card{background:var(--bg);border:1px solid var(--line);border-radius:var(--radius);padding:28px;display:flex;flex-direction:column;gap:12px;transition:.35s var(--ease);position:relative;overflow:hidden}
  .card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--hue);opacity:.85}
  .card:hover{transform:translateY(-4px);border-color:var(--hue)}
  .card .tag{align-self:flex-start;font-family:var(--mono);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px;border-radius:5px;color:var(--hue);background:var(--hue-soft)}
  .card h3{font-size:1.45rem}
  .card p{color:var(--text-2);font-size:.94rem;flex:1}
  .card .go{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:.92rem;color:var(--hue)}
  .card .go .arrow{transition:.25s}
  .card:hover .go .arrow{transform:translateX(4px)}
  .card small.dom{font-family:var(--mono);font-size:.68rem;color:var(--muted);letter-spacing:.04em}

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
  .mini-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
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
    .cards,.proc-grid,.feature-grid{grid-template-columns:1fr}
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
        % (p["hue"], p["slug"], p["name"], p["domain"]) for p in PRODUCTS
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
  "description": "ZET8 makes finished, ready-to-use apps for small businesses — Ponchi workforce management, Deskomigo mobile back office, Zet8 CRM, LocalSave local deals, and OnSMS text-based hiring.",
  "email": "hello@zet8.com",
  "address": {"@type": "PostalAddress","addressLocality": "Houston","addressRegion": "TX","addressCountry": "US"},
  "parentOrganization": {"@type": "Organization","name": "Optima Buildsolutions LLC"},
  "sameAs": ["https://ponchi.app","https://deskomigo.com","https://crm.zet8.com","https://localsave.com","https://onsms.com"]
}
</script>
<style>%(css)s</style>
</head>
<body>
""" % {"title": title, "desc": desc, "path": path, "site": SITE, "css": CSS}


def page(title, desc, path, content, logo_b64, current="", extra_js=""):
    return (head(title, desc, path) + nav(logo_b64, current) + content + footer()
            + "<script>" + JS + extra_js + "</script>\n</body>\n</html>\n")


# ----------------------------------------------------------------- home page
def home_content(logo_b64):
    cards = "".join("""
      <a class="card hue-%s reveal" href="/%s/">
        <span class="tag">%s</span>
        <h3>%s</h3>
        <p>%s</p>
        <span class="go">Learn more <span class="arrow">→</span></span>
        <small class="dom">%s</small>
      </a>""" % (p["hue"], p["slug"], p["cat"], p["name"], p["card"], p["domain"]) for p in PRODUCTS)
    return """
<section class="hero">
  <div class="wrap hero-inner">
    <img class="hero-logo reveal" src="data:image/png;base64,%s" alt="ZET8 — tech solutions for businesses">
    <h1 class="reveal d1">Ready-to-use apps that run your small business.</h1>
    <p class="sub reveal d2">No custom builds, no six-month projects. ZET8 makes finished software products — workforce management, back office, sales, local deals, and on-demand hiring. Sign up and start today.</p>
    <div class="hero-cta reveal d3">
      <a href="#products" class="btn btn-primary">See the apps <span class="arrow">→</span></a>
      <a href="/about/" class="btn btn-ghost">About ZET8</a>
    </div>
    <div class="hero-meta reveal d4">
      <span>Ready today</span><span>Free trials</span><span>Mobile-first</span><span>AI built in</span>
    </div>
  </div>
</section>

<section id="products">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="eyebrow mono"><span class="dot" style="background:var(--yellow)"></span>Products</div>
      <h2>Five apps. One job: run the business better.</h2>
      <p>Finished products — built, shipped, and run by ZET8. Pick one and start today.</p>
    </div>
    <div class="cards">%s</div>
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
""" % (logo_b64, cards)


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
      <a class="btn btn-hue" href="%(url)s" target="_blank" rel="noopener">Visit %(domain)s <span class="arrow">→</span></a>
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
    <a class="btn btn-hue" href="%(url)s" target="_blank" rel="noopener">Get started <span class="arrow">→</span></a>
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
        "about": p["about"], "url": p["url"], "domain": p["domain"],
        "pricing": p["pricing"], "pricing_html": p["pricing"].replace("·", "<b>·</b>"),
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
    <div class="prose reveal">
      <p><b>We don't do custom projects.</b> Every ZET8 product is a finished app you can sign up for today — born from real problems we watched real businesses fight: time theft on job sites, invoices written at midnight, leads going cold in spreadsheets, empty shifts with no one to call.</p>
      <p><b>We build for the phone in your pocket.</b> Your office is a truck cab, a counter, a job site. Everything we ship works one-handed on a phone first — in English and Español.</p>
      <p><b>We use AI where it erases busywork.</b> Scanning receipts, drafting summaries, flagging follow-ups — not another chatbot between you and your work.</p>
      <p class="legal-note">ZET8 is operated by Optima Buildsolutions LLC · Houston, Texas</p>
    </div>
  </div>
</section>
<section class="family" style="padding-top:0">
  <div class="wrap">
    <h2 class="reveal">The ZET8 family</h2>
    <div class="mini-cards" style="grid-template-columns:repeat(5,1fr)">@@MINIS@@</div>
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
                <option>Zet8 CRM — sales pipeline</option>
                <option>LocalSave — local deals</option>
                <option>OnSMS — on-demand hiring</option>
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


def main():
    with open(os.path.join(HERE, "logo-wide-transparent-clean.png"), "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("ascii")

    def write(rel, html):
        path = os.path.join(HERE, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        io.open(path, "w", encoding="utf-8").write(html)
        print("wrote", rel, "(%d bytes)" % len(html))

    # home
    home = page("ZET8 — Tech Solutions for Businesses",
                "ZET8 makes finished, ready-to-use apps for small businesses — Ponchi workforce management, Deskomigo mobile back office, Zet8 CRM, LocalSave local deals, and OnSMS text-based hiring.",
                "/", home_content(logo_b64), logo_b64)
    write("index.html", home)

    # product pages
    for p in PRODUCTS:
        title = "%s — %s | ZET8" % (p["name"], p["tagline"].rstrip("."))
        desc = p["card"] + " " + p["pricing"] + "."
        write("%s/index.html" % p["slug"],
              page(title, desc, "/%s/" % p["slug"], product_content(p), logo_b64))

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

    # sitemap
    urls = ["/"] + ["/%s/" % p["slug"] for p in PRODUCTS] + ["/about/", "/contact/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join("  <url><loc>%s%s</loc><changefreq>weekly</changefreq></url>\n" % (SITE, u) for u in urls)
    sm += "</urlset>\n"
    write("sitemap.xml", sm)

    # artifact preview: home page with absolute links so navigation works from the preview
    write("artifact-preview.html", home.replace('href="/', 'href="%s/' % SITE).replace('href="%s/#' % SITE, 'href="#'))


if __name__ == "__main__":
    main()
