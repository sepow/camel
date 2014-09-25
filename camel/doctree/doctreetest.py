#------------------------------------------------
# main
#------------------------------------------------
import doctree

def main(args=None):
    
    # process command line arguments
    from optparse import OptionParser
    op = OptionParser()
    (options,args) = op.parse_args()
    if not args:
        print 'usage: $python doctree.py main.tex (camel.cls)'
        return
    latex_main_file = args[0]

    # open input file
    with open(latex_main_file) as f:
        latex_str = f.read()

    # initialise tree 
    tex_tree = doctree.TexTree( latex_main_file )

    # output
    print '==============================================='
    print tex_tree
    print '==============================================='
    print tex_tree.prettyprint_xml()
    print '==============================================='
    print tex_tree.labels
    print '==============================================='

    # traverse
    # traverse(tex_tree)

if __name__ == '__main__':
    main()

