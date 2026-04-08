# Pre-Release Checklist

## Core Health

- [ ] Backend is running on `127.0.0.1:8001`
- [ ] Frontend is running on `127.0.0.1:3000`
- [ ] Nginx is routing correctly on port `80` / `443`
- [ ] PostgreSQL is running on `127.0.0.1:5432`
- [ ] Redis is running on `127.0.0.1:6379`

## Admin Checks

- [ ] Local admin responds:
  - `curl -I http://127.0.0.1:8001/admin/`
- [ ] Nginx admin responds:
  - `curl -I http://127.0.0.1/admin/`
- [ ] Live admin responds:
  - `curl -I https://library.digigalaxy.cloud/admin/`
- [ ] Admin static CSS loads:
  - `curl -I https://library.digigalaxy.cloud/static/admin/css/custom-admin.62a49925f149.css`
- [ ] Admin login page renders correctly in browser
- [ ] Account dropdown opens above the page content
- [ ] Admin login/logout works
- [ ] One model list page opens correctly

## Frontend Checks

- [ ] Local frontend root responds:
  - `curl -I http://127.0.0.1:3000/`
- [ ] Live frontend root responds:
  - `curl -I https://library.digigalaxy.cloud/`
- [ ] Home page opens without `500`
- [ ] Login page opens:
  - `/login`
- [ ] Register page opens:
  - `/register`
- [ ] Localized auth routes open:
  - `/ar/login`
  - `/ur/register`

## Auth And JWT

- [ ] Login returns tokens:
```bash
RESPONSE=$(curl -s -X POST http://127.0.0.1:8001/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@library.local","password":"Admin123!Change"}')

echo "$RESPONSE"
```

- [ ] Access token extraction works:
```bash
ACCESS_TOKEN=$(printf '%s' "$RESPONSE" | python3 -c 'import sys, json; print(json.load(sys.stdin)["tokens"]["access"])')
echo "$ACCESS_TOKEN"
```

- [ ] Protected user endpoint works:
```bash
curl -s http://127.0.0.1:8001/api/v1/users/me/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

- [ ] Refresh token endpoint works:
```bash
REFRESH_TOKEN=$(printf '%s' "$RESPONSE" | python3 -c 'import sys, json; print(json.load(sys.stdin)["tokens"]["refresh"])')

curl -s -X POST http://127.0.0.1:8001/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$REFRESH_TOKEN\"}"
```

- [ ] Browser login works from `/login`
- [ ] Browser registration works from `/register`
- [ ] Registration redirects to `/dashboard`
- [ ] Login redirects to `/dashboard`

## Security Checks

- [ ] Replace weak Django/JWT signing secret with a strong random value
- [ ] Confirm `DEBUG=False` in production
- [ ] Confirm secure cookie flags are enabled
- [ ] Confirm HTTPS is active on live domain
- [ ] Confirm admin is not exposed on unintended hosts

## Recommended Improvements Before Final Production

- [ ] Move auth from `localStorage` to `HttpOnly` secure cookies if stronger browser-side security is required
- [ ] Add token rotation / blacklist policy if refresh-token revocation is needed
- [ ] Add a simple smoke test script for auth and homepage checks
- [ ] Add monitoring for backend and frontend process health

## Native Dev Start Commands

Backend:
```bash
cd /home/fg/library-platform
./scripts/dev-backend.sh
```

Frontend:
```bash
cd /home/fg/library-platform/frontend
npm run dev
```

Worker:
```bash
cd /home/fg/library-platform
./scripts/dev-worker.sh
```

Beat:
```bash
cd /home/fg/library-platform
./scripts/dev-beat.sh
```
