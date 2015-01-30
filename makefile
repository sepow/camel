# makefile for camel website 
# 

PYTHON = /Users/scmde/environments/camel/bin/python
ROOT = /Users/scmde/sites/camel/camel


all : 
	$PYTHON $(ROOTDIR)/manage.py runserver


install : all 
	-echo 'yes' | python manage.py collectstatic

clean :
	-echo 'clean up'

