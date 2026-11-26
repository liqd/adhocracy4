# Cap captcha integration

`adhocracy4.captcha` integrates the self-hosted [Cap](https://trycap.dev)
captcha. It provides a Django form field and widget, server-side token
verification and a React component used by polls.

The existing Captcheck integration is unchanged and remains available through
`A4_CAPTCHA_TYPE = "captcheck"`.

## Configuration

| Setting | Purpose |
| --- | --- |
| `A4_CAPTCHA_TYPE` | `"captcheck"` (default) or `"cap"` |
| `A4_CAP_CAPTCHA_ENDPOINT` | Public Cap site endpoint, e.g. `https://cap.example.com/<site-key>/` |
| `A4_CAP_CAPTCHA_SITEVERIFY_URL` | Optional server-side verification URL; defaults to `<endpoint>/siteverify` |
| `A4_CAP_CAPTCHA_SECRET` | Cap secret key, server-side only |
| `A4_CAP_CAPTCHA_WIDGET_URL` | Widget script URL |
| `A4_CAP_CAPTCHA_WASM_URL` | Optional self-hosted proof-of-work WASM URL |
| `A4_CAP_CAPTCHA_HASHWX_URL` | Optional self-hosted HashWX WASM URL |
| `A4_CAPTCHA_TIMEOUT` | Verification request timeout in seconds (default `5`) |
| `CAPTCHA_TEST_ACCEPTED_ANSWER` | Test-only bypass value |

Cap is enabled for forms when `A4_CAPTCHA_TYPE = "cap"` and the endpoint,
secret and widget URL are configured. Polls additionally show the captcha for
unregistered users when the poll allows it.

## Current verification behaviour

`verify_cap_token()` sends the widget token to Cap's `/siteverify` endpoint and
treats the token as valid only when the response contains `"success": true`.

Verification fails closed when:

- the configuration is incomplete
- the Cap service is unreachable or times out
- Cap rejects the token
- the token is missing, expired or already used

A rejected token prevents form submission or poll voting. Cap handles token
expiry and single use.

## Risk flags and instrumentation

Cap can return additional fields from `/siteverify`, such as `riskFlags`,
`behavior.score` and `behavior.verdict`. **The current adhocracy4 integration
does not evaluate these fields.** It only checks `success`.

Therefore:

- a solve that Cap flags but does not block is accepted
- flags do not trigger additional email verification, account deactivation or
  any other application-side action
- flags, verdicts and scores are recorded only by the Cap Standalone instance,
  in its events/dashboard and logs
- Cap records technical context such as token ID, flags, score, verdict, IP and
  ASN, but does not know the Django user or email address
- blocking only happens when the Cap site key itself blocks the solve; in that
  case no valid token is issued and the backend rejects the submission

Instrumentation is not implemented as custom application code. The official
widget runs instrumentation challenges automatically when they are enabled on
the site key. New Cap keys enable instrumentation by default.

## Content Security Policy

Under a strict CSP, Cap's widget needs nonces for the scripts and styles it
injects, including the instrumentation iframe:

- `window.CAP_SCRIPT_NONCE`
- `window.CAP_CSS_NONCE`

The current integration does not pass a CSP nonce. If the enforcing CSP blocks
inline scripts or styles, instrumentation and widget styling can fail even
though the rest of the widget is allowed.

The widget also requires `connect-src` access to the Cap endpoint (and to the
WASM URL if it is not self-hosted) plus `script-src-elem` access to the widget
script URL. WebAssembly may additionally require `'wasm-unsafe-eval'`.

## Privacy

When Cap is self-hosted, the challenge and verification traffic stays on the
platform. The integration does not log the token or secret. Token verification
failures are logged as warnings without user identity or personal data.
