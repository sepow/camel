# -*- coding: utf-8 -*-

'''
refresh.py (camel/management)

steps:
1. create doctree: parse main.py
2. traverse doctree: populate database

'''

import os, re, time, shutil, logging, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from camel.doctree import *
from camel.models import Module, TreeNode

SITE_ROOT = getattr(settings, 'SITE_ROOT')
TEX_ROOT  = getattr(settings, 'TEX_ROOT')

out = logging.getLogger(__name__)

class Command(BaseCommand):
    args = 'module_code (, module_code, ...)'
    help = 'Update database for specified module codes'
    
    def handle(self, *args, **options):
        
        # process argument (module code)
        if not args:
            print 'Usage: python manage.py refresh MAXXXX'
            return
        
        # info
        timestr = time.strftime("%Y.%m.%d.%H.%M.%S")
        out.info('Logging started at %s', timestr)
        out.info('SITE_ROOT = %s' % SITE_ROOT)
        out.info('TEX_ROOT  = %s' % TEX_ROOT)
        
        for module_code in args:
            out.info('BEGIN processing %s', module_code)
            
            # find main.tex
            main_tex = os.path.join(TEX_ROOT, module_code, 'main.tex')
                        
            # create book tree
            book = Book(main_tex)
            
            # hack to set newcommands
            nc = ''
            nc += r'\newcommand{\N}{\mathbb{N}}'
            nc += r'\newcommand{\R}{\mathbb{R}}'
            nc += r'\newcommand{\prob}{\mathbb{P}}'
            nc += r'\newcommand{\expe}{\mathbb{E}}'
            nc += r'\newcommand{\var}{\text{Var}}'
            nc += r'\newcommand{\cov}{\text{Cov}}'
            nc += r'\newcommand{\supp}{\text{supp}}'

            # extract module information (from main.tex preamble)
            minfo = extract_module_info( main_tex )
            
            # set commit flag
            commit = True
    
            # check whether this module already exists in the database
            modules = camel.models.Module.objects.filter(year=minfo['year'], code=minfo['code'])
            if not modules:
                print 'Module does NOT exist in the database...creating it'
                mo = camel.models.Module(year=minfo['year'], code=minfo['code'], title=minfo['title'])
                mo.save()
            elif len(modules) > 1:
                print 'More than one module with this year and code exists in the database...PROBLEM!'
                commit = False
            else:
                print 'Module DOES exist in the database...book will be hooked on'
                mo = modules[0]

            # set module newcommands (hack)
            mo.newcommands = nc
            mo.save()
            
            # output tree to database
            book.camel_tree(module=mo, commit=commit)

            # TODO sort out labels/references/citations

