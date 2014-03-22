#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, re, logging, json

logging.root.setLevel(logging.ERROR)

class TeuxDeux:
  cookies={}
  headers={}

  def __handle(self, r):
    logging.debug(r.headers)
    logging.debug(r.text)
    assert r.status_code!=401,"Unable to authenticate"
    self.cookies = requests.utils.dict_from_cookiejar(r.cookies)

  def get(self, url):
    r = requests.get('https://teuxdeux.com/'+url,
      cookies=self.cookies,
      headers=self.headers)
    self.__handle(r)
    return r

  def post(self, url, data=None):
    r = requests.post('https://teuxdeux.com/'+url, 
      data=data,
      cookies=self.cookies,
      headers=self.headers)
    self.__handle(r)

  def __init__(self, login, password):
    r=self.get("login")
    
    tokens = re.findall(r"<input type=\"hidden\" name=\"authenticity_token\" value=\"(.*)\">",r.text)
    assert len(tokens)>0,"Unable to find authenticity_token on login page"
    self.headers = {"X-Csrf-Token":tokens[0]}

    payload = {
      "authenticity_token": tokens[0],
      "username": login,
      "password": password}
    
    self.post("login", payload)


  def create_todo(self, todo, do_on):
    payload = json.dumps({
      "id":None,
      "current_date":do_on,
      "list_id":None,
      "text":todo,
      "done":False,
      "deleted_at":None})

    self.post("api/v1/todos", payload)


  def list_todos(self, fro, to):
    r=self.get("api/v1/todos/calendar?begin_date=%s&end_date=%s" % (fro,to))    
    return r.text