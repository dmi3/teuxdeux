#TeuxDeux Unofficial API

Since there are no news on [TeuxDeux API](https://github.com/teuxdeux/teuxdeux-api), here's quick'n'dirty hack with most basic functions: authentication, post and list todos. Can be simply extended if other features are required.

##Requirements:

* [Requests](http://docs.python-requests.org/en/latest/user/install/#install) `pip install requests`

##Usage:

    from TeuxDeux import TeuxDeux
  
    td=TeuxDeux("login","password")
    print(td.list_todos("2014-03-16","2014-03-30"))
    td.create_todo("The ToDo","2014-03-22") 