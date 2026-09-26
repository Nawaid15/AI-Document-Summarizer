import os
import base64
from email.message import EmailMessage

# Google Auth and Workspace Libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Modern 2026 Google Gemini GenAI SDK
from google import genai


# Google API scopes required by this project
VALID_SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]


def get_google_credentials():
    """Authenticates the user and returns Google OAuth credentials."""
    creds = None

    # Check for existing OAuth token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            VALID_SCOPES
        )

    # If credentials are missing or invalid, authenticate again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                VALID_SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for future runs
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds


def get_google_doc_text(document_id, creds):
    """Reads and extracts raw text from a Google Doc."""

    # Connect to Google Docs API
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().get(
        documentId=document_id
    ).execute()

    content = doc.get("body", {}).get("content", [])

    # Extract text from paragraphs
    text = ""

    for element in content:
        if "paragraph" in element:
            for paragraph_element in element["paragraph"].get("elements", []):
                if "textRun" in paragraph_element:
                    text += paragraph_element["textRun"].get(
                        "content",
                        ""
                    )

    return text


def generate_summary(text_content):
    """Processes raw document text through Gemini 2.5 Flash."""

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing GEMINI_API_KEY environment variable!"
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "Create a detailed and visually engaging email summary of the following document.\n\n"

            "The output will be sent directly as the body of an email.\n\n"

            "STRICT OUTPUT RULES:\n"
            "1. Output ONLY the final email content. Do not explain your instructions.\n"
            "2. NEVER use *** this marks in between scentences. or donot start scentnence with '*' in the bottom  or in the middle not even a single line should start or end with '*' \n"
            "3. NEVER use Markdown formatting.\n"
            "4. NEVER use asterisks (*) anywhere in the output.\n"
            "5. NEVER use underscores (_) for formatting.\n"
            "6. NEVER use backslashes (\\) for formatting or escaping.\n"
            "7. NEVER use Markdown headings such as #, ## or ###.\n"
            "8. NEVER use Markdown bold, italic, code blocks, tables, or Markdown links.\n"
            "9. NEVER write placeholders such as 'Your Name', 'Your Name/Team Name', "
            "'Team Name', '[Your Name]', '[Name]', or similar placeholders.\n"
            "10. NEVER include HTML, image URLs, emoji URLs, or image syntax.\n"
            "11. Use real Unicode emojis directly, such as 🔬 🧪 💧 📊 🎯 ✅ ⚠️ 🌊.\n"
            "12. Do NOT write emojis as links. For example, NEVER write "
            "[🔬](https://...). Write only 🔬.\n"
            "13. The final output must look like a clean, professionally formatted "
            "plain-text email.\n\n"

            "VISUAL STYLE:\n"
            "• Start with an attractive emoji-based title.\n"
            "• Use emoji-based section headings.\n"
            "• Put this separator between major sections:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "• Use • for bullet points.\n"
            "• Use numbered lists for procedures and steps.\n"
            "• Use emojis naturally throughout the content.\n"
            "• Use around 2-5 relevant emojis in substantial sections.\n"
            "• Use arrows such as ➡️, ⬇️, ⬆️ when they help explain a process or relationship.\n"
            "• Use visual labels such as:\n"
            "📌 KEY POINT\n"
            "💡 NOTE\n"
            "📊 RESULT\n"
            "⚠️ IMPORTANT\n"
            "✅ CONCLUSION\n"
            "• Keep enough spacing between sections so the email is easy to scan.\n\n"

            "IMPORTANT:\n"
            "Do not add a greeting such as 'Hello team' unless it is genuinely "
            "appropriate for the document.\n"
            "Do not add a fake sign-off.\n"
            "Do not add 'Best regards'.\n"
            "Do not add a sender name or team name at the end.\n"
            "End naturally after the actual summary content.\n\n"

            "CONTENT RULES:\n"
            "• Preserve important names, numbers, observations, procedures, findings, "
            "and conclusions.\n"
            "• Do not invent information.\n"
            "• Keep the summary detailed but easier to read than the original document.\n"
            "• Make the email interesting and visually engaging without excessive emoji spam.\n\n"

            "DOCUMENT TO SUMMARIZE:\n\n"
            f"{text_content}"
        )
    )

    summary = response.text

    # Remove unwanted Markdown formatting
    summary = summary.replace("\\*", "")
    summary = summary.replace("**", "")
    summary = summary.replace("*", "")
    summary = summary.replace("__", "")
    summary = summary.replace("_", "")

    return summary.strip()

def send_email_summary(summary_text, recipient_email, creds):
    """Sends the summary using the Gmail API."""

    sender_email = os.environ.get("SENDER_EMAIL")

    if not sender_email:
        raise ValueError(
            "Missing SENDER_EMAIL environment variable!"
        )
        # Create email
        message = EmailMessage()

        message.set_content(summary_text)

        message["To"] = recipient_email
        message["From"] = sender_email
        message["Subject"] = "✨ Automated AI Document Summary"

        # Gmail API expects the MIME message as base64URL
        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        # Connect to Gmail API
        service = build(
            "gmail",
            "v1",
            credentials=creds
        )

        # Send the email
        send_message = (
            service.users()
            .messages()
            .send(
                userId="me",
                body={"raw": encoded_message}
            )
            .execute()
        )

        return send_message


if __name__ == "__main__":

    DOC_ID = os.environ.get("GOOGLE_DOC_ID")
    TO_EMAIL = os.environ.get("TO_EMAIL")

    if not DOC_ID:
        raise ValueError(
            "Missing GOOGLE_DOC_ID environment variable!"
        )

    if not TO_EMAIL:
        raise ValueError(
            "Missing TO_EMAIL environment variable!"
        )

    try:
        print("🔐 Initializing Google Authentication...")

        # Authenticate once and reuse the same credentials
        creds = get_google_credentials()

        print("📄 Reading Google Document...")
        doc_text = get_google_doc_text(DOC_ID, creds)

        if not doc_text.strip():
            print("⚠️ The targeted Google Document appears to be empty.")

        else:
            print("🤖 Generating summary via Gemini 2.5 Flash...")

            summary = generate_summary(doc_text)

            print("✉️ Dispatching email summary via Gmail API...")

            send_email_summary(
                summary,
                TO_EMAIL,
                creds
            )

            print("🎉 Success! Check your inbox.")

    except Exception as e:
        import traceback
        print("\n❌ Execution Error:")
        traceback.print_exc()
