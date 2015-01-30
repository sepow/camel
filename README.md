--
## CAMEL: CArdiff Mathematics E-Learning
--

### Directory Structure

/root
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
			- refresh.py	# update database
			- update.py		# update pdf
	
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
	
	logs/
	
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

	tex/ -> /path/to/tex_root
	
	texmf/
		- camel.cls
		- camel.sty
		- arholiad.sty


