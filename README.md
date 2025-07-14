# validate\_mail

A lightweight Python web service to validate email addresses using syntax checks, MX record lookups, and optional SMTP verification.

## Features

* **Regex-based syntax validation**: Ensures email addresses conform to RFC-compliant formatting.
* **MX record validation**: Confirms the existence of mail servers for the email domain.
* **SMTP verification (optional)**: Attempts a real SMTP connection to check if the address is deliverable.
* **Flask-based**: Provides a simple HTTP API for integration.
* **HTML front‑end**: Basic UI form (located in `templates/`) for manual email checks.
* **Deployable**: Configuration available for platforms like Vercel.

---

## Getting Started

### Prerequisites

* Python 3.8+
* `pip` (or `pipenv` / Poetry)

### Installation

```bash
git clone https://github.com/ShubhamM3958/validate_mail.git
cd validate_mail
pip install -r requirements.txt
```

---

## Usage

Run the web service:

```bash
python app.py
```

By default, the Flask server will start on `http://localhost:5000`.
Navigate there to access the web form and validate email addresses interactively.

---

## API Reference

**Endpoint**: `POST /validate`
**Request Body** (JSON):

```json
{
  "email": "user@example.com",
  "check_mx": true,
  "verify": true
}
```

| Field      | Type    | Description                                              |
| ---------- | ------- | -------------------------------------------------------- |
| `email`    | string  | The email address to validate                            |
| `check_mx` | boolean | Check MX (mail server) records                           |
| `verify`   | boolean | If true, perform SMTP-level verification after MX lookup |

**Response** (JSON):

```json
{
  "valid_syntax": true,
  "mx_valid": true,
  "smtp_verified": false,
  "deliverable": false,
  "message": "MX record found; SMTP server not reachable"
}
```

Field definitions:

* `valid_syntax`: Is the email format valid?
* `mx_valid`: Does the domain have MX records?
* `smtp_verified`: Could the address be verified via SMTP?
* `deliverable`: Overall deliverability (true if all checks passed).
* `message`: Human-readable summary of validation result.

---

## Project Structure

```
validate_mail/
├── app.py             # Flask web app & API
├── requirements.txt   # Required Python dependencies
├── templates/
│   └── index.html     # Front‑end form
└── vercel.json        # (Optional) Vercel deployment settings
```

---

## Dependencies

* **Flask** – Web server framework for the UI and API.
* **dnspython** – Perform DNS MX record lookups.
* **smtplib** – Built-in library for SMTP protocol interactions.

---

## Examples

**cURL request**:

```bash
curl -X POST http://localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","check_mx":true,"verify":false}'
```

Expected response:

```json
{
  "valid_syntax": true,
  "mx_valid": true,
  "smtp_verified": null,
  "deliverable": true,
  "message": "Syntax valid; MX record found"
}
```

---

## Deployment

To deploy on Vercel or similar platforms:

* Ensure `vercel.json` is configured to route to `app.py`.
* Install dependencies via `requirements.txt`.
* Specify runtime (e.g., Python 3.10) in deploy config.

---

## Suggested Improvements

* Add unit and integration tests.
* Add request rate limiting.
* Implement caching for DNS/Sender verifications.
* Expand SMTP error handling and fallback retry logic.
* UI enhancements: show result statuses via colors/icons.

---

## License

*Add your license here (e.g. MIT, Apache 2.0).*
*(If you didn't include a License file, consider adding one for clarity.)*

---

## Contributions

Pull requests and feedback are welcome!
Please open an issue to propose major changes.
