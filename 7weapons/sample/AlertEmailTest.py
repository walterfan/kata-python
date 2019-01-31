import os,sys

current_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_path, "../util")
sys.path.append(lib_path)

import EmailSender
import FileLogger


def quickTest(emailSender, emailReceiver, **kwargs):

    recipients = [emailReceiver]

    mdLogger = FileLogger.MarkdownLogger('test.md')

    mdLogger.print("# Pager duty alert test email")

    mdLogger.print("\n\n")
    mdLogger.printTableTitle(['date', 'pool', 'error count'])
    mdLogger.printTableRow(['2018-8-1', 'tsj01', 3000])
    mdLogger.printTableRow(['2018-8-2', 'tsj01', 4000])
    mdLogger.printTableRow(['2018-8-3', 'tsj01', 5000])
    mdLogger.printTableRow(['2018-8-4', 'tsj01', 6000])
    mdLogger.printTableRow(['2018-8-5', 'tsj01', 7000])

    mdLogger.print("\n\n")

    sender = EmailSender.EmailSender(emailSender, **kwargs)

    sender.sendWithImages("Production Alert Email", recipients, mdLogger.toHtml(), "../template/email_template.j2")

if __name__ == '__main__':

    quickTest(os.getenv('EMAIL_USER'), 'fanyamin@hotmail.com', mailServer=os.getenv('EMAIL_SMTP_SERVER'), mailPort=587,
              needLogin=True, useTls=True, username=os.getenv('EMAIL_USER'), password=os.getenv('EMAIL_PWD'))