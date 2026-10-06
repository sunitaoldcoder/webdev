# Install Shivam Agri AI on a phone

A PWA installs from its HTTPS website. No APK or Play Store upload is required.
The computer's localhost URL cannot be used as the public mobile app address.
The installable MVP still uses demo advisory/vision and sample market/weather unless
real providers are configured; installation does not turn samples into live data.

## Deploy one web service and a database (example: Render)

1. Sign in to Render with your GitHub account and allow access to
   `sunitaoldcoder/webdev`. No credentials should be entered in this chat.
2. Create a managed PostgreSQL database. Choose region and plan deliberately;
   hosting, persistent disks and database plans may cost money. Review the price
   and any expiry/sleep limits before creating resources.
3. Create a Web Service using the repository and branch `shivam-agri-ai-mvp`.
   Choose Docker. Leave the root directory empty and use the root `Dockerfile`.
   This image builds React and serves Django/API/PWA from the same origin.
4. Configure service environment variables securely in the hosting dashboard:

   | Name | Value |
   | --- | --- |
   | DEBUG | `0` |
   | DJANGO_SECRET_KEY | A new random secret, not the local demo value |
   | DATABASE_URL | Managed PostgreSQL connection URL; copy securely from provider |
   | TRUST_PROXY_HEADERS | `1` for Render's trusted HTTPS reverse proxy only |
   | WEATHER_PROVIDER | `sample` initially, `open_meteo` after verifying API access |
   | MEDIA_ROOT | `/var/data/media` with a persistent private disk mounted at `/var/data` |

   Generate a Django secret locally in Command Prompt using:
   `.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   Copy it into the dashboard, not chat or GitHub. The Render external hostname is
   automatically added to allowed hosts and trusted CSRF origins. For another
   host set ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS explicitly for your HTTPS domain.
   Use your database provider's required certificate/trust settings for external
   PostgreSQL connections; never disable certificate checks to work around failure.
5. Set the health check path to `/healthz`. Attach the persistent disk before
   inviting farmers, so uploaded photos survive deployments. It must stay private:
   only authenticated API routes may serve crop images.
6. Deploy. Startup runs migrations and creates the crop catalogue. It does NOT
   create demo farmer or staff logins. Register your own farmer through the app.
7. Confirm the HTTPS website opens, registration works, the crop choices appear,
   and the Crop Doctor can upload a photo. Confirm photos persist after a restart.
   Test staff accounts separately; create one with `python manage.py createsuperuser`
   from the hosting shell, using a mobile-format username for the app's staff login.

For a custom domain, configure ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS for that domain
and let your host issue an HTTPS certificate. Set appropriate backup, privacy,
account recovery/phone verification, staff-role and data-retention policies before
using the MVP with real farmers. Keep the demo limitations visible.

## Android installation

1. Open the deployed HTTPS website in Chrome on the phone.
2. If the Hindi install button appears, tap **ऐप इंस्टॉल करें** and confirm.
3. Otherwise open Chrome's three-dot menu and choose **Install app** or
   **Add to Home screen**. The label differs across Chrome versions.
4. Open Shivam Agri AI from its home-screen icon and register/log in.

The install banner appears only when the browser provides an installation prompt.
An already installed app or unsupported browser may not show it. If it is absent,
check HTTPS, manifest/icon requests and the browser menu.

## iPhone installation

1. Open the HTTPS website in Safari.
2. Tap Share → Add to Home Screen (on newer iOS this may also be in the menu).
3. Enable Open as Web App if offered, then tap Add.

## Offline behavior and updates

Only the public app shell is cached. Farmer records, crop images, API results and
admin content are not cached. Chat, registration, weather and market requests need
internet access; the app cannot provide new advice offline. Voice recognition and
available Hindi voices depend on the phone/browser and microphone permission.
When publishing a new shell release, bump the CACHE version in public/sw.js so the
new shell/assets are cached. Close and reopen the app after an update.

## Testing the unified deployment locally

Build React and collect static assets, then run the backend. The built PWA is served
at the backend root, including its manifest and service worker:

```bat
npm --prefix frontend ci
npm --prefix frontend run build
.venv\Scripts\python.exe backend\manage.py collectstatic --noinput
.venv\Scripts\python.exe backend\manage.py runserver 8000
```

On the same Windows computer, the localhost site can be tested. Installing on
farmers' phones still needs the deployed HTTPS website, not a localhost address.
