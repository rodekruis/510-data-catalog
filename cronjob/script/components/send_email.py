from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .config import ENV


def send_mail(to_emails, email_content):
    message = Mail(
        from_email="crm@510.global",
        to_emails=to_emails,
        subject="510 Data Catalog: Dataset Update Required",
        plain_text_content=email_content)
    # print(email_content)

    try:
        sg = SendGridAPIClient(api_key=str(ENV['SENDGRID_API_KEY']))
        response = sg.send(message)
        return response
    except Exception as e:
        raise e


def generate_email_content(resource_name, path, url):
    content = """
Dear data owner,

The data resource '{}' is not available at location '{}'.
Please update the location of the data in the Data Catalog.

You can find the resource at:
{}

Thanks in advance,
510 Data Catalog

    """.format(resource_name, path, url)

    return content
