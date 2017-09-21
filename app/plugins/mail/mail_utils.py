import config
import email
import imaplib
 

def decode_header(encoded_header):
    decoded = list()
    for (encoded, charset) in email.header.decode_header(encoded_header):
        if isinstance(encoded, str):
            decoded.append(encoded)
        elif isinstance(encoded, bytes):
            decoded.append(encoded.decode(charset or 'utf8'))
    return ''.join(decoded)


def get_new_messages():
    new_msgs = []

    try:
        mail = imaplib.IMAP4_SSL(config.mail_server)
        (retcode, capabilities) = mail.login(config.mail_login, config.mail_password)
        mail.list()
        mail.select('inbox')

        (retcode, messages) = mail.search(None, '(UNSEEN)')
        if retcode == 'OK':
            for num in messages[0].split():
                typ, data = mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        original = email.message_from_bytes(response_part[1])

                        mail_from = decode_header(original['From'])
                        mail_subj = decode_header(original['Subject'])
                        new_msgs.append( (mail_from, mail_subj) )

    except:
        print("[!] Failed to get mail list")

    return new_msgs
