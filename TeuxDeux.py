#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, re, logging, json, datetime

logging.root.setLevel(logging.ERROR)

class TeuxDeux:
  find_authenticity_token = r"<input[^<>]*?name=\"authenticity_token\"[^<>]*?value=\"(.*)\""
  date_fmt = "%Y-%m-%d"
  cookies={}
  headers={}

  def __handle(self, r):
    logging.debug(r.headers)
    logging.debug(r.text)
    assert r.status_code != 401, "Unable to authenticate"

    self.cookies = requests.utils.dict_from_cookiejar(r.cookies)

  def get(self, url):
    r = requests.get('https://teuxdeux.com/'+url,
      cookies = self.cookies,
      headers = self.headers)
    self.__handle(r)
    return r.text

  def post(self, url, data = None):
    r =requests.post('https://teuxdeux.com/' + url, 
      data = data,
      cookies = self.cookies,
      headers = self.headers)
    self.__handle(r)

  def __init__(self, login, password):
    login_page = self.get("login")
    
    tokens = re.findall(self.find_authenticity_token, login_page)
    assert len(tokens)>0, "Unable to find authenticity_token on login page"    
    self.headers = {"X-Csrf-Token": tokens[0]}

    credentials = {
      "authenticity_token": tokens[0],
      "username": login,
      "password": password}
    
    self.post("login", credentials)


  def create(self, text, do_on = datetime.date.today(), done = False):
    todo = json.dumps({
      "id": None,
      "current_date": do_on.strftime(self.date_fmt),
      "list_id": None,
      "text": text,
      "done": done,
      "deleted_at": None})

    self.post("api/v1/todos", todo)


  def list(self, begin = datetime.date.today(), end = datetime.date.today()):
    todos=self.get("api/v1/todos/calendar?begin_date=%s&end_date=%s" % 
      (begin.strftime(self.date_fmt), end.strftime(self.date_fmt)))    
    
    return json.loads(todos)

