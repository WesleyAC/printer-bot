#!/usr/bin/env python3

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re
import os
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Server(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode())

        # https://daringfireball.net/2010/07/improved_regex_for_matching_urls
        urls = re.findall(r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""" , data["data"])

        outs = []
        for url in urls:
            print(url[0])
            dl = urlopen(url[0]).read()
            name = "attach." + url[0].split(".")[-1]
            with EmailSenderThingy("recurse.printer.bot@gmail.com", os.environ["PRINTER_BOT_PASSWORD"]) as server:
                server.send_message(from_addr='recurse.printer.bot@gmail.com',
                        to_addrs=['awi29aibu5676@hpeprint.com'],
                        msg='',
                        subject='',
                        attachments=[(name, dl)])
            outs.append(url[0])

        out_msg = str.format(
            """Hi! <3

I've printed the following urls:

{urls}

Have a nice day :leaves: :sparkles:""", urls=outs)
    
        response = json.dumps({"content": out_msg}).encode()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
        self.wfile.flush()
        print("foo")

# https://alexwlchan.net/2016/05/python-smtplib-and-fastmail/
class EmailSenderThingy(smtplib.SMTP_SSL):
    """A wrapper for handling SMTP connections to FastMail."""

    def __init__(self, username, password):
        super().__init__('smtp.gmail.com', port=465)
        self.login(username, password)

    def send_message(self, *,
                     from_addr,
                     to_addrs,
                     msg,
                     subject,
                     attachments=None):
        msg_root = MIMEMultipart()
        msg_root['Subject'] = subject
        msg_root['From'] = from_addr
        msg_root['To'] = ', '.join(to_addrs)

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)
        msg_alternative.attach(MIMEText(msg))

        if attachments:
            for attachment in attachments:
                prt = MIMEBase('application', "octet-stream")
                prt.set_payload(attachment[1])
                encoders.encode_base64(prt)
                prt.add_header(
                    'Content-Disposition', 'attachment; filename="%s"'
                    % attachment[0].replace('"', ''))
                msg_root.attach(prt)

        self.sendmail(from_addr, to_addrs, msg_root.as_string())

if __name__ == "__main__":
    s = HTTPServer(("", 8080), Server)
    s.serve_forever()
