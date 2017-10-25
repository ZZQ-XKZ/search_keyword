from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(tags=None, title=None, text=None, file=None, image=None):
        subject = ''
        if tags:
                for tag in tags:
                        subject += '[' + tag + ']'

        if subject.find('[bwg]') == -1:
                subject = '[bwg]' + subject
                
        if title:
                subject += title

        if file:
                input_file = open(file, 'r')
                try:
                        text = input_file.read()
                finally:
                        input_file.close()

        msg = MIMEMultipart()
        if text.find('html'):
                msg.attach(MIMEText(text, 'html', 'utf-8'))
        else:
                msg.attach(MIMEText(text, 'plain', 'utf-8'))
        msg['To'] = _format_addr('blackfe <%s>' % 'blackfe2010@gmail.com')
        msg['From'] = _format_addr('BWG <%s>' % 'blackfe2010@gmail.com')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        if image:
                image_file = open(args.image, 'rb')
                image = MIMEImage(image_file.read())
                image_file.close()
                msg.attach(image)

        server = smtplib.SMTP("localhost")
        server.set_debuglevel(1)
        server.sendmail(
                'blackfe2010@gmail.com',
                'blackfe2010@gmail.com',
                msg.as_string())
        server.quit()


if __name__ == '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('--tag')
        parser.add_argument('--title')
        parser.add_argument('--text')
        parser.add_argument('--file')
        parser.add_argument('--image')
        args = parser.parse_args()
        tags = args.tag.split(',')
        send_email(tags, args.title, args.text, args.file, args.image)
