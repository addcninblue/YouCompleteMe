#!/usr/bin/env python

from bs4 import BeautifulSoup
from markdown import markdown
import fileinput
import re

def ContentToIdValue( content ):
  content = content.replace( ' ', '-' )
  return re.sub( r'[^\w_-]+', '', content ).lower()


def AddIdsForHeadings( soup ):
  def AddIds( headings ):
    for heading in headings:
      heading[ 'id' ] = ContentToIdValue( heading.get_text() )

  for i in xrange( 1, 7 ):
    AddIds( soup.find_all( 'h' + str( i ) ) )
  return soup

markdown_lines = list( fileinput.input() )

# We delete the first two lines because that's the big YCM heading which we
# already have on the page
del markdown_lines[:2]

markdown_source = ''.join( markdown_lines )

with open('index.html', 'r+') as content_file:
  content = content_file.read()

  new_contents = markdown( unicode( markdown_source, 'utf-8' ),
                           extensions=['fenced_code'] )
  new_tags = AddIdsForHeadings( BeautifulSoup( new_contents, 'html5lib' ) )

  soup = BeautifulSoup( content, 'html5lib' )
  elem = soup.find( id='markdown-output' )
  elem.clear()
  for new_elem in new_tags.body.contents:
    elem.append( new_elem )

  content_file.seek( 0 )
  content_file.truncate()
  content_file.write( str( soup ) )

