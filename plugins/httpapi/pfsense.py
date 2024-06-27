from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
name: pfsense
short_description: Use httpapi to run command on pfsense appliances
description: This connection plugin provides a connection to remote devices over HTTP(S).
version_added: 2.7.2
author: Philipp Lomosits
seealso:
- plugin: ansible.plugins.httpapi
  plugin_type: httpapi
"""

from functools import wraps
import lxml.html
import re
from urllib.error import HTTPError
import urllib.parse

from ansible.errors import AnsibleAuthenticationFailure
from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.urls import prepare_multipart

from ansible.plugins.httpapi import HttpApiBase

__all__ = ["HttpApi", "ensure_csrf"]


def ensure_csrf(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if self.csrfMagicToken is None:
            self.get("/")
        return func(self, *args, **kwargs)

    return wrapped


# https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/httpapi.py
class HttpApi(HttpApiBase):
    csrfMagicToken = None

    def get(self, path, **kwargs):
        return self.send_request(
            None,
            method="GET",
            path=path,
            **kwargs
        )

    @ensure_csrf
    def post(self, path, data: dict, **kwargs):
        return self.send_request(
            data,
            method="POST",
            path=path,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            **kwargs
        )

    @ensure_csrf
    def post_multipart_form_data(self, path, data: dict, **kwargs):
        return self.send_request(
            data,
            method="POST",
            path=path,
            headers={
                "Content-Type": "multipart/form-data",
            },
            **kwargs
        )

    def send_request(self, data, **kwargs):

        if kwargs.get("method") == "POST":
            if kwargs.get("headers")["Content-Type"] == "application/x-www-form-urlencoded":
                data = urllib.parse.urlencode(
                    ({"__csrf_magic": self.csrfMagicToken} if self.csrfMagicToken is not None else {}) | data or {})
            elif kwargs.get("headers")["Content-Type"] == "multipart/form-data":
                multipart = prepare_multipart(
                    ({"__csrf_magic": self.csrfMagicToken} if self.csrfMagicToken is not None else {}) | data or {})
                kwargs = kwargs | {
                    "headers": kwargs.get("headers", {}) | {"Content-Type": multipart[0]}
                }
                data = multipart[1]

        try:
            response, response_data = self.connection.send(
                "/" + kwargs.get("path", "").lstrip("/"),
                data,
                **{k: v for k, v in kwargs.items() if k not in ["path"]}
            )
        except HTTPError as exc:
            return exc.code, exc.read()

        try:
            return self.handle_response(response, response_data)
        except ApplyNeeded:
            return self.send_request(
                {
                    "apply": "Applay Changes"
                },
                method="POST",
                path=kwargs.get("path", ""),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            )

    @ensure_csrf
    def login(self, username, password):

        try:
            response, response_data = self.post(
                "/",
                {
                    "__csrf_magic": self.csrfMagicToken,
                    "usernamefld": username,
                    "passwordfld": password,
                    "login": "Sign In"
                },
                follow_redirects=False
            )

            if response.code != 302:
                raise AnsibleAuthenticationFailure(message="Failed to login.")

        except HTTPError as exc:
            return exc.code, exc.read()

    def logout(self):
        # self.get("/index.php?logout")
        self.connection._auth = None

    def update_auth(self, response, response_text):
        return _build_cookie_header(response.info().get("Set-Cookie"))

    def handle_response(self, response, response_data):
        # read response
        response_data = response_data.read()
        if len(response_data) == 0:
            return response, response_data

        decoded_response_data = response_data.decode("utf-8")

        # get csrfMagicToken for the next request
        result = re.search(r"csrfMagicToken = \"(sid[^\"]*)\"", decoded_response_data)
        if result is not None and result.group(1) is not None:
            self.csrfMagicToken = result.group(1)

        html = lxml.html.fromstring(decoded_response_data)

        # check for input-errors
        input_errors = html.xpath("//div[contains(@class,'input-errors')]/ul/li/text()")
        if input_errors:
            raise Exception("\n".join(input_errors))

        # check if apply is needed
        apply_button = html.xpath("//form//button[@type='submit' and @name='apply']")
        if apply_button:
            raise ApplyNeeded()

        if isinstance(response, HTTPError):
            raise ConnectionError(to_text(response), code=response.code)

        return response, response_data


def _build_cookie_header(cookie_header):
    if cookie_header:
        index_of_semicolon = cookie_header.find(";")
        if index_of_semicolon != -1:
            cookie_header = cookie_header[0:index_of_semicolon]
        return {"Cookie": cookie_header}
    return None


class ApplyNeeded(Exception):
    pass
