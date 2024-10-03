from flask import Flask, render_template, request, jsonify
import re
import smtplib
import dns.resolver
import threading

app = Flask(__name__)


def is_valid_email_syntax(email):
    regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(regex, email) is not None


def get_mx_record(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return mx_records[0].exchange.to_text()  # Return first MX record
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return None


def validate_email_smtp(email):
    global server
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    if not mx_record:
        return False, "No MX record found for domain"

    try:
        server = smtplib.SMTP(timeout=30)
        server.set_debuglevel(0)

        # SMTP handshake
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        code, message = server.rcpt(email)

        if code == 250:
            return True, "Email address is valid"
        else:
            return False, f"Email address is not valid"

    except smtplib.SMTPServerDisconnected:
        return False, "SMTP server disconnected unexpectedly"
    except smtplib.SMTPConnectError:
        return False, "Failed to connect to SMTP server"
    except smtplib.SMTPRecipientsRefused:
        return False, "Recipient refused"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    finally:
        if 'server' in locals():
            server.quit()


# Main email validation function
def validate_email(email):
    if not is_valid_email_syntax(email):
        return False, "Invalid email format"

    return validate_email_smtp(email)


@app.route('/', methods=['GET', 'POST'])
def index():
    email = None
    result = None

    # Check if the form is submitted
    if request.method == 'POST':
        email = request.form.get('email')
    elif request.args.get('email'):
        email = request.args.get('email')

    if email:
        is_valid, message = validate_email(email)
        result = {'email': email, 'is_valid': is_valid, 'message': message}

    return render_template('index.html', result=result)


# Route for validating email via API (JSON response)
# @app.route('/api/validate', methods=['GET'])
# def api_validate_email():
#     email = request.args.get('email')
#     if not email:
#         return jsonify({'error': 'No email provided'}), 400
#
#     is_valid, message = validate_email(email)
#     return jsonify({'email': email, 'is_valid': is_valid, 'message': message})
@app.route('/api/validate', methods=['GET'])
def api_validate_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'No email provided'}), 400

    # Run validation in a background thread
    result = {}
    thread = threading.Thread(target=lambda: result.update(validate_email(email)))
    thread.start()
    thread.join(timeout=10)  # Wait for 10 seconds

    if not result:  # If no result is returned
        return jsonify({'email': email, 'is_valid': False, 'message': "Validation timed out"}), 504

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False)
