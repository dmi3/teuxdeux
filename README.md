#TeuxDeux Unofficial API

Since there are no news on [TeuxDeux API](https://github.com/teuxdeux/teuxdeux-api), here's quick'n'dirty hack with most basic functions: authentication, post and list todos. Can be simply extended if other features are required.

##Requirements:

* [Requests](http://docs.python-requests.org/en/latest/user/install/#install) `pip install requests`

##Usage:
    from datetime import date,timedelta
    from TeuxDeux import TeuxDeux
  
    tomorrow = date.today() + timedelta(days=1)  

    td=TeuxDeux("username","password")

    td.create("todo today")
    td.create("todo tomorrow", tomorrow)

    for td in td.list(end = tomorrow):
      print td['text']