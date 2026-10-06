# Shivam Agri AI — AI Advisory Platform for Farmers

Hindi-first, mobile-first agriculture advisory MVP for Lucknow, Rae Bareli,
Gorakhpur and Varanasi. English navigation and registration are available;
Hindi is the primary product language. Some secondary screens remain Hindi.

## What works

- Registration: name, Indian mobile number, password, district, village, language,
  multiple crops, acreage and irrigation. No Aadhaar, date of birth or address collected.
- Token login/logout, farmer-owned profile and farms, multiple crops and farm addition.
- Educational chat with farmer context, voice input, read-aloud, feedback and expert escalation.
- Crop Doctor: phone camera/file upload, validated JPEG/PNG/WEBP, private image access,
  possible issue / low confidence / next steps / expert referral.
- Weather: clearly labeled five-day sample data, or credential-free Open-Meteo API.
- Mandi: filter crop/district/market, min/max/modal, date, source, update time,
  sample label and saved prices. Live prices are explicitly unavailable.
- My Farm: recent questions, diagnoses, saved prices, subscription and alerts empty state.
- Staff-only analytics charts, feedback and expert case response/resolution.
- PWA shell (manifest/service worker); API data is never cached for offline use.
- WhatsApp disabled endpoint and reusable text router seam.

**This is a working local/demo MVP, not a deployed production advisory system.**
The default chat and vision providers are safe deterministic demos, not a real
LLM or disease model. Vision does not infer diseases from an image. Never use
sample prices/weather to make farm decisions. No live expert network is connected.

> AI-based advisory. Verify important crop-treatment decisions with a qualified
> agriculture expert/KVK.

## Architecture

```text
Farmer → React / TypeScript / Tailwind / PWA → Django REST API
                                               ├─ account & farm services
                                               ├─ advisory → LLMProvider
                                               ├─ diagnosis → VisionProvider
                                               ├─ weather → WeatherProvider
                                               ├─ market → MarketPriceProvider
                                               ├─ expert cases / feedback / analytics
                                               └─ PostgreSQL (SQLite for quick local demo)
Browser voice → speech recognition → normal advisory API → speech synthesis
Future WhatsApp transport → verified webhook → MessageRouter → same services
```

`backend/` contains separate Django apps: accounts, farmers, farms, advisory,
crop_diagnosis, weather, market_prices, experts, feedback, subscriptions, whatsapp,
analytics. Models have audit timestamps and committed migrations. Service classes
own registration, farm writes, advisory, diagnosis, expert replies and analytics.
`providers/interfaces.py` defines replaceable LLM, vision, weather, market, STT and
TTS contracts; `providers/factory.py` is the composition root. Injectable providers
can be tested without paid credentials. Open-Meteo is the implemented live adapter.
LLM/vision/official-market adapters are future work, not silently activated by keys.
The browser is the current voice adapter; speech support varies by browser/device
and may require an internet connection. No voice audio is stored by this backend.

`frontend/src/` separates pages, shared components, API client and language catalog.
Add Bhojpuri to `i18n.ts`, registration language choices and voice locale/provider
mapping when a tested Bhojpuri speech service is available.

## Quick local setup (Python 3.12+, Node 20.19+ / 22.12+)

Use the existing repository checkout. Cloud tasks are already isolated; do not
create a Git worktree unless explicitly requested.

```bash
cd /workspace/webdev                 # or your local clone
cp .env.example .env                 # only if .env does not already exist
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py seed_demo
npm --prefix frontend ci
```

The backend loads the root `.env` without overriding existing process variables.
For this quick workflow leave `POSTGRES_HOST` unset: it uses `backend/db.sqlite3`.
`seed_demo` is repeatable; it doesn't reset existing passwords or overwrite users.
It requires `DEMO_PASSWORD` and creates crops Wheat, Rice/Paddy, Mustard, Potato,
Tomato and Pulses, plus four labeled demo farmers:

| District | Mobile / login | Default local demo password |
| --- | --- | --- |
| Lucknow | 9000000000 | FarmerDemo2026 |
| Rae Bareli | 9000000001 | FarmerDemo2026 |
| Gorakhpur | 9000000002 | FarmerDemo2026 |
| Varanasi | 9000000003 | FarmerDemo2026 |

These are fictional local accounts, not real people. Change `DEMO_PASSWORD` before
seeding if desired. Do not expose demo accounts to the public internet.

Run in two terminals:

```bash
# terminal 1
.venv/bin/python backend/manage.py runserver 0.0.0.0:8000
# terminal 2
npm --prefix frontend run dev
```

Locally open port 5173. Vite proxies `/api` to port 8000. Cloud onboarding has no
localhost preview links; validate with internal requests. Phone camera/microphone
need HTTPS or a trusted localhost context; browser permission and Hindi voice
availability are required. Unsupported speech browsers offer text fallback.

## Admin and expert dashboard

For a production-managed account use `python backend/manage.py createsuperuser`.
Django admin is at `/admin/`. The application staff login uses the same backend
username through the mobile login field; create a staff account with a mobile-format
username to use the React staff dashboard.

For an explicitly opt-in **local demo** staff account:

```bash
.venv/bin/python backend/manage.py seed_demo --with-admin
```

This creates login `9000000099` using `DEMO_PASSWORD`, without resetting an existing
user. Login shows the Administration menu and a staff expert queue. Staff can see
all cases, download private images, reply and mark cases resolved. Farmers only see
their own cases. Staff privilege is shared by admins and experts in this MVP;
separate roles and assignment queues are future work.

## Environment variables

See `.env.example` (never commit `.env` or tokens).

| Variable | Purpose |
| --- | --- |
| DEBUG | 1 for local only; set 0 before deployment |
| DJANGO_SECRET_KEY | Unique deployment secret; demo default rejected with DEBUG=0 |
| ALLOWED_HOSTS | Comma-separated backend hostnames |
| DEMO_PASSWORD | Explicit fictional-account seed password |
| POSTGRES_HOST | Set to switch from SQLite to PostgreSQL |
| POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD | PostgreSQL connection settings |
| WEATHER_PROVIDER | `sample` (default) or `open_meteo` |
| LLM_API_KEY / VISION_API_KEY | Reserved placeholders for future adapters; no automatic activation |
| WHATSAPP_* | Reserved for future verified Meta transport; webhook remains disabled |

Live weather needs HTTPS access to `api.open-meteo.com`. Failures return HTTP 503;
no invented or silently substituted weather. Weather explanation is deterministic
and based on API fields, with suggestions clearly separate from observations.
Official market API integration should retain commodity, mandi, min/max/modal,
price date, source, updated time and unavailable state. The LLM never supplies prices.

## PostgreSQL and Docker

```bash
cp .env.example .env                 # preserve an existing .env
# choose a database password in .env
docker compose up --build -d
docker compose exec backend python manage.py test advisory providers
docker compose exec backend python manage.py seed_demo --with-admin
```

Frontend is on local port 8080; backend on 8000. PostgreSQL 16 is private to the
Compose network. Database/media volumes persist; running containers do not survive
cloud snapshots and must restart. Backend startup runs migrations and seeds demo
accounts, then Gunicorn. This Compose file is for local MVP demonstration; remove
demo seeding and harden infrastructure before production. Set DEBUG=0, unique
secrets, HTTPS, secure cookie settings, restricted hosts, backups, at-rest encryption,
retention/deletion procedures and proper staff roles before collecting real data.
No claims of production security certification are made.

## API contracts

Success: `{"data": ...}`; errors: `{"error": ...}`. JSON requests except crop images
(multipart). Private endpoints require `Authorization: Token <token>` or an
appropriate authenticated Django session. Login/register are rate-limited.

| Endpoint | Purpose |
| --- | --- |
| POST /api/auth/register, /api/auth/login, /api/auth/logout | Account lifecycle |
| GET/PATCH /api/farmers/me | Own profile and history |
| GET/POST/PATCH /api/farms | Own farms and crops |
| POST /api/advisory/ask | `{question}` → labeled demo advisory and message_id |
| POST /api/crop-diagnosis | image, crop, description; 5MB / 20MP cap |
| GET /api/crop-diagnosis/:id/image | Private owner/staff image download |
| GET /api/weather?district=Lucknow | Provider-backed weather |
| GET/POST /api/market-prices?crop=Wheat&district=Lucknow&market=... | Fetch/save provider result |
| POST /api/feedback | message_id, boolean helpful, optional comment |
| GET/POST /api/expert-cases | Own requests (all for staff) |
| POST /api/expert-cases/:id/respond | Staff response and resolved flag |
| GET /api/admin/analytics | Staff-only summary |
| POST /api/whatsapp/webhook | Disabled, returns 503 |

Passwords are hashed by Django. Farmer-owned queries enforce ownership, images
are not publicly served, logs include method/path/status/timing but no token,
question, profile or image contents. Session tokens are held in sessionStorage and
revoked on logout. Mobile ownership verification, password reset and token expiry
are future production work. Reverse proxy and rate limits should protect public APIs.

## Tests and validation

```bash
.venv/bin/python backend/manage.py check
.venv/bin/python backend/manage.py makemigrations --check --dry-run
.venv/bin/python backend/manage.py test advisory providers
npm --prefix frontend run build
```

Backend tests cover registration, private access, ownership, risky demo guidance,
feedback, image validation, sample labeling, admin/expert permissions, logout,
disabled WhatsApp and live-weather adapter behavior with mocked HTTP responses.
Frontend build performs TypeScript checks. Browser smoke checks verify the Hindi
login/chat/feedback/weather/market/My Farm workflow and mobile overflow.
Microphone/camera hardware and live AI disease accuracy are not automated claims.

## Future WhatsApp setup

Keep the endpoint disabled until a production adapter implements Meta webhook
challenge verification, HMAC signature validation, replay/idempotency checks,
mobile identification and opt-in, media validation/download limits, and approved
outbound transport. Configure credentials securely in environment settings; never
embed keys in source. `whatsapp/services.py` routes text into the existing advisory
service; add voice/image/location/menu handlers through the same service contracts.
Do not expose an unverified webhook or promise human response times.

Future FPO, government, subscription, Bhojpuri, soil, satellite and IoT features can
be added as separate modules using these farmer/service/channel boundaries.

## Current cloud verification

11 backend tests passed against SQLite, PostgreSQL and the Docker backend.
TypeScript/production build, migrations, demo API smoke and mobile browser flows
passed. Live Open-Meteo access was rejected by the cloud egress policy (HTTP 403),
so only the sample weather workflow and mocked live-adapter contract are verified.
Allow `api.open-meteo.com` in environment settings before switching to live weather.

Cloud Docker builds behind an intercepting proxy may require proxy build arguments,
a resolved proxy hostname in build `extra_hosts`, and the environment's public CA
bundle through the optional `proxy_ca` BuildKit secret. Do not disable TLS checking.
These machine-specific settings are not embedded in the application images.

Run a representative API smoke check after starting the app:

```bash
.venv/bin/python scripts/smoke.py
```

## Installable phone app (PWA)

See [PWA installation and hosting steps](docs/PWA-INSTALL.md). The root Dockerfile
packages the frontend and API into one service, with no automatic demo accounts.
Django serves the built PWA using WhiteNoise; HTTPS is enforced with DEBUG=0.
A Hindi install banner appears when the browser offers installation. Android users
can also install through Chrome's menu; iPhone users use Safari's Add to Home Screen.
Publishing requires your hosting account, managed PostgreSQL and persistent private
image storage. This repository has not been deployed to a public website.

Hosting checks: `python backend/manage.py test advisory providers config`.
