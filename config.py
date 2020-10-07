#!/usr/bin/env python

# import config_secrets (best to make this a symlink to .ssh/config_secrets.py
import config_secrets

'''Configuration for the EMailSender module.

Use this module's classes to include and customize the config.
'''

class Base:
    '''Incorporates the Global Variables in the derivative classes.

    'smtp_secrets': username and password.
    'smtp_config': for sending emails.
    'recipient_info': for sending run reports to the administrator.
    'plaintext_message': for formatting the plain text.
    'html_message': for formatting the richtext message text.
    '''
    def __init__(self):
        self.smtp_secrets = config_secrets.Sending_Account
        self.smtp_config = {'host': 'smtp.colorado.edu',
                            'port': 587,
                            'login_id': self.smtp_secrets['login_id'],
                            'passwd': self.smtp_secrets['passwd']}
        self.recipient_info = {'first': 'Some',
                               'last': 'Person',
                               'email_address': ['Some.Person@Colorado.EDU']}
        self.plaintext_message = '''EMailSender Message
Message generated on: {date}.

Name: {first} {last}

{message_text}

Notes:
    {footer}'''
        self.html_message = '''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Invoice</title>
    
    <style>
    .invoice-box {{
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
        font-size: 16px;
        line-height: 24px;
        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        color: #555;
    }}
    
    .invoice-box table {{
        width: 100%;
        line-height: inherit;
        text-align: left;
    }}
    
    .invoice-box table td {{
        padding: 5px;
        vertical-align: top;
    }}
    
    .invoice-box table tr td:nth-child(2) {{
        text-align: right;
    }}
    
    .invoice-box table tr.top table td {{
        padding-bottom: 20px;
    }}
    
    .invoice-box table tr.top table td.title {{
        font-size: 45px;
        line-height: 45px;
        color: #333;
    }}
    
    .invoice-box table tr.information table td {{
        padding-bottom: 40px;
    }}
    
    .invoice-box table tr.heading td {{
        background: #eee;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
    }}
    
    .invoice-box table tr.details td {{
        padding-bottom: 20px;
    }}
    
    .invoice-box table tr.item td {{
        border-bottom: 1px solid #eee;
    }}
    
    .invoice-box table tr.item.last td {{
        border-bottom: none;
    }}
    
    .invoice-box table tr.total td:nth-child(2) {{
        border-top: 2px solid #eee;
        font-weight: bold;
    }}
    
    @media only screen and (max-width: 600px) {{
        .invoice-box table tr.top table td {{
            width: 100%;
            display: block;
            text-align: center;
        }}
        
        .invoice-box table tr.information table td {{
            width: 100%;
            display: block;
            text-align: center;
        }}
    }}
    
    /** RTL **/
    .rtl {{
        direction: rtl;
        font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    }}
    
    .rtl table {{
        text-align: right;
    }}
    
    .rtl table tr td:nth-child(2) {{
        text-align: left;
    }}
    </style>
</head>

<body>
    <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">
            <tr class="top">
                <td colspan="2">
                    <table>
                        <tr>
                            <td class="title">
                                EMailSender Message
                            </td>
                            
                            <td>
                                &nbsp;
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            
            <tr class="information">
                <td colspan="2">
                    <table>
                        <tr>
                            <td>
                                Message generated on: {date}<br />
                            </td>
                            
                            <td>
                                Name: {first} {last}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            
            <tr class="heading">
                <td>
                    Message
                </td>
                
                <td>
                    &nbsp;
                </td>
            </tr>
            
            <tr class="item">
                <td>
                    Text:
                </td>
                
                <td>
                    {message_text}
                </td>

            </tr>

            <tr class="heading">
                <td>
                    Notes
                </td>
                
                <td>
                    &nbsp;
                </td>
            </tr>
            
            <tr class="information">
                <td colspan="2">
                    {footer}&nbsp;
                </td>
            </tr>
        </table>
    </div>
</body>
</html>'''


class Production(Base):
    '''Fetch data, build email message, and send.'''
    def __init__(self):
        Base.__init__(self)

class Development(Base):
    '''Fetch data, build email message, and send.'''
    def __init__(self):
        Base.__init__(self)