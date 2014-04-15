import re
import sys
import os
import getopt
class CommentsHandler:
    def __init__(self):

        """ remove c/cpp-style comments.
            text: blob of text with comments (can include newlines)
            returns: text with comments removed
        """
        #http://perldoc.perl.org/perlfaq6.html#How-do-I-use-a-regular-expression-to-strip-C-style-comments-from-a-file%3f
        self.pattern = r"""
                                ##  --------- COMMENT ---------
               /\*              ##  Start of /* ... */ comment
               [^*]*\*+         ##  Non-* followed by 1-or-more *'s
               (                ##
                 [^/*][^*]*\*+  ##
               )*               ##  0-or-more things which don't start with /
                                ##    but do end with '*'
               /                ##  End of /* ... */ comment
             |                  ##  C++ style comment
             //                 ##  start with //
             ([^\\]|[^\n][\n]?) ## Not a line endingg with a '\'
             *?\n               ## One line
             |                  ##  -OR-  various things which aren't comments:
               (                ##
                                ##  ------ " ... " STRING ------
                 "              ##  Start of " ... " string
                 (              ##
                   \\.          ##  Escaped char
                 |              ##  -OR-
                   [^"\\]       ##  Non "\ characters
                 )*             ##
                 "              ##  End of " ... " string
               |                ##  -OR-
                                ##
                                ##  ------ ' ... ' STRING ------
                 '              ##  Start of ' ... ' string
                 (              ##
                   \\.          ##  Escaped char
                 |              ##  -OR-
                   [^'\\]       ##  Non '\ characters
                 )*             ##
                 '              ##  End of ' ... ' string
               |                ##  -OR-
                                ##
                                ##  ------ ANYTHING ELSE -------
                 .              ##  Anything other char
                 [^/"'\\]*      ##  Chars which doesn't start a comment, string
               )                ##    or escape
        """
        self.regex = re.compile(self.pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)

    def remove_comments(self, text):
        noncomments = [''];
        #noncomments = [m.group(3) for m in regex.finditer(text) if m.group(3)]
        for m in self.regex.finditer(text):
            if m.group(2):
                noncomments.append('\n');
            if m.group(3):
                noncomments.append(m.group(3))

        return "".join(noncomments)
    def remove_comments_of_file(self, src_file, target_file):
        if not os.path.isfile(src_file):
            return;
        try:
            sh = open(src_file,'rb')
            if not sh:
                print("cannot open src_file:" + src_file)
                return
            code_bytes = sh.read();
            try:
                code_with_comments = code_bytes.decode('utf-8')
            except UnicodeDecodeError:
                code_with_comments = code_bytes.decode('GBK','ignore')

            code_without_comments = self.remove_comments(code_with_comments)
            sh.close()
            code_without_comments=code_without_comments.encode('utf-8' )

            fh = open(target_file, "wb")
            if not fh:
                print("Cannot open target_file for write:" + target_file)
                return

            fh.write(code_without_comments)
            fh.close()
        except IOError as err:
            print('IO exception: ' + str(err))



def get_file_list(dir):
    l = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            l.append(os.path.join(root, name))
    return l

def filter_file_list(flist, filter_string):
    #pattern = re.compile(r'.*cs$')
    l = []
    pattern = re.compile(filter_string)
    for f in flist:
        if(pattern.match(f)):
            l.append(f)
    return l;

def remove_all_comments(srcdir, targetdir, file_filter):
    if(not os.path.isdir(srcdir)):
        print('srcdir:' + srcdir + 'is not a directroy')
        return
    #Make target dir
    if(not os.path.isdir(targetdir)):
        os.makedirs(targetdir)

    handle = CommentsHandler()
    l = get_file_list(srcdir)
    l = filter_file_list(l, file_filter)
    for f in l:
        target_file = os.path.join(targetdir, f);
        target_file_dir = os.path.dirname(target_file)
        if(not os.path.isdir(target_file_dir)):
            os.makedirs(target_file_dir)
        print( '=============>' + f)
        handle.remove_comments_of_file(f, target_file)

        print(target_file)

if __name__ == '__main__':
    try:
        indir = 'scripts'
        outdir = 'tmp'
        opts,args=getopt.getopt(sys.argv[1:], 'i:o:',['indir=','outdir='])
        for o, a in opts:
            if o in ('-i', '--indir'):
                indir=a;
            elif o in ('-o', '--outdir'):
                outdir=a;
            else:
                print(system.argv[0] + '-i indir -o outdir')
    except getopt.GetoptError as err:
        print('exception: ' + str(err))

    remove_all_comments(indir,outdir,r'.*cs$')
    print("===================Done")
    exit()
