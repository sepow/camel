--
## CAMEL: CArdiff Mathematics E-Learning
--

### Directory Structure

	.git/
	.gitignore
	
	camel/
		admin.py
		doctree.py
		models.py
		settings.py
		urls.py
		views.py
		wsgi.py
	
		management/
			- refresh.py	    # update database
			- update.py		    # update pdf
			- readsims.py		# read students enrolled on module
	
	data/
        pdf/
            MA0000/
                notes.pdf
                notes-with-blanks.pdf
                slides.pdf
        /sims
            MA0000_students.csv
        /tex
            MA0000/
                camel.cls -> ../../texmf/camel.cls
                camel.sty -> ../../texmf/camel.sty
                main.tex
                references.bib

	fixtures/
		users.json
		modules.json
		books.json
	
	static/
		base.css
		camel_logo.png

	templates/
		- base.html
		- index.html
		- modules.html
		- module-detail.html
		- chapter-detail.html
		- login.html
		- logout-success.html

	texmf/
		- camel.cls
		- camel.sty

### manage.py commands

##### $ python manage.py refresh MODULE_CODE --options
	Refresh the database (content) for module MODULE_CODE
	Options:
		-t:	write module doctree, text format to stdout
		-x: write module doctree, xml format to stdout
		-d: pretend write to database
		-commit: real write to database
		
##### $ python manage.py cohort MODULE-CODE ACADEMIC-YEAR 
	Cohort specified by MODULE_CODE and ACADEMIC_YEAR
	Looks for a file modulecode_academicyear.xls in the XLS_ROOT
	
##### $ python manage.py import-cohort modulecode-academicyear.xls
	Cohort specified by MODULE_CODE and ACADEMIC_YEAR
	Cohort needs to be defined initially by ma1500_1415.xls, containing just a list of students
	Can import and export
	e.g. ma1500_1415.xls contains 
		1. student id
		2. assessment 1 (mark inc binary)
		list of studentsRefresh the user-module (many-to-many) tables database (content) for module MODULE_CODE
	Options:
		-t:	write module doctree, text format to stdout
		-x: write module doctree, xml format to stdout
		-d: pretend write to database
		-commit: real write to database
		
### How-To

##### Re-install the database from scratch (from xml files)
1. $ rm SITE_ROOT/data/camel.db
2. $ python manage.py readsims students.xml
3. $ python manage.py refresh MA0000 --commit 