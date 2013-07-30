#! /usr/bin/python

from HTMLParser import HTMLParser

is_tag_tt = False  # Indicates data for this tag is being read.
class MyHTMLParser(HTMLParser):
    
    
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        if tag == 'tt': is_tag_tt = True
        
        for attr in attrs:
            print "     attr:", attr
    def handle_endtag(self, tag):
        print "End tag  :", tag
        if tag == 'tt': is_tag_tt = False
        
    def handle_data(self, data):
        #if is_tag_tt == True:
        print "Data     :", data
        
    def handle_comment(self, data):
        print "Comment  :", data
        pass
        
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
        pass
    
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
        pass
    
    def handle_decl(self, data):
        print "Decl     :", data
        pass

parser = MyHTMLParser()

def parse_output(content):
    """
    1)remove bold html tags: <B></B>
    2)Remove '&nbsp;'
    """
    content = content.replace('<B>','').replace('</B>','').replace('<U>','').replace('</U>','').replace('&nbsp;','')
#    print content
#    print 'number of lines', len(content.split('\n'))
#    lines=content.split('\n')
#    for l in lines:
#        print '*', l.strip()


    parser.feed(content)

def get_hist_formatted(d_len):
    """
    """
    plen_list = range(7, 15)
    count_list = []
    for plen in plen_list:
        count = 0
        if d_len.has_key(plen)==True:
            count = d_len[plen]
        count_list.append(count)
    count_list
    return count_list

from bs4 import BeautifulSoup
def parse_w_soup(content):
    ligand_list = []
    is_read_ligand = False
    
    content = content.replace('<B>','').replace('</B>','').replace('<U>','').replace('</U>','').replace('&nbsp;','')
    soup = BeautifulSoup(content, "html5lib")
    #print(soup.prettify())
    
    #print soup.head
    #print soup.tt
    #for a in  soup.find_all('a'):
    #for a in  soup.find_all('tt'):
    for row in  soup.find_all('tr'):
        #print '*', row
        #print '*', str(row)
        if 'Example' in str(row): 
            is_read_ligand = True
            #print 'Example!!'
            #print row
        elif 'T-cell epitope' in str(row):
            is_read_ligand = False 
            #print 'T-cell!!'
            #print row
        else: 
            #print '*'
            pass
        if is_read_ligand == True:
            tt_list = row.find_all('tt')
            for tt in tt_list:
                #print is_read_ligand, tt, tt.string
                ligand_list.append(tt.string)
        #result = a.find_all('tt')
        #print '**', result
    ligand_list = list(set(ligand_list))
    ligand_list = map(str,ligand_list)
    return ligand_list
    
def count_length(peptide_list):
    d = {} # d[length] = count
    for peptide in peptide_list:
        plen = len(peptide)
        count = d.get(plen, 0) + 1
        d[plen] = count
    return d

def run():
    header = ['mhc'] + range(7, 15)
    print '\t'.join(map(str, header))
    
    fname_list = open('fname_list.txt','r').readlines()
    for fname in fname_list:
        content = open(fname.strip(),'r').read()
        ligand_list = parse_w_soup(content)
        d_len = count_length(ligand_list)
        row = [fname.strip()] + get_hist_formatted(d_len)
        print '\t'.join(map(str, row))

if __name__ == '__main__':
    run()
#    
#    #fname = 'output.txt'
#    #fname = 'output.HLA-A-0201.txt'
#    fname = 'output.H-2-Db.html'
#    content = open(fname,'r').read()
#    #parse_output(content)
#    ligand_list = parse_w_soup(content)
#    d_len = count_length(ligand_list)
#    print d_len
#    print map(str,ligand_list)