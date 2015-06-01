# file: camel/__init__.py
#    executes when package (app) is loaded

# expose selected classes (for modules in other apps)
# e.g "from camel import Book" instead of "from camel.doctree import Book"
# from doctree import Book

# startup
default_app_config = 'myapp.apps.MyAppConfig'

