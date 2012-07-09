#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Xibo - Digitial Signage - http://www.xibo.org.uk
# Copyright (C) 2009 Alex Harrington
#
# This file is part of Xibo.
#
# Xibo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version. 
#
# Xibo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Xibo.  If not, see <http://www.gnu.org/licenses/>.
#

from BrowserMediaBase import BrowserMediaBase
from threading import Thread
import urllib
import sys, os, time

class BrowserMediaAnimatedBase(BrowserMediaBase):
        
    def injectContent(self):
        """ Returns a string of content to inject in to the page """
        content = ""
        
        items = self.getContent()
        count = 0
        
        for tmpItem in items:
            count += 1
            if self.options['direction'] == 'left' or self.options['direction'] == 'right':
                tmpItem = tmpItem.replace('<p>','')
                tmpItem = tmpItem.replace('</p>','')
                tmpItem = tmpItem.replace('<p/>','')
                tmpItem = tmpItem.replace('<br>','')
                tmpItem = tmpItem.replace('<br/>','')
                tmpItem = tmpItem.replace('<div>','')
                tmpItem = tmpItem.replace('</div>','')
                tmpItem = tmpItem.replace('<div/>','')
                
                tmpItem = "<span class='article'>%s</span>" % tmpItem
            else:
                tmpItem = "<div class='XiboRssItem'>%s</div>" % tmpItem
            
            content += tmpItem
        
        self.itemCount = count

        # Add in the Copyright Text (if applicable)
        try:
            content += self.options['copyright']
        except:
            pass
        
        
        if self.options['direction'] == 'none':
            pass
        else:
            if self.options['direction'] == 'left' or self.options['direction'] == 'right':
                content = "<nobr>%s</nobr>" % content
            
            if self.options['direction'] == 'single':
                content = "<div id='text'>%s</div>" % content
            else:
                content = '<div id="contentPane" style="overflow: none; width:%spx; height:%spx;"><div id="text">%s</div></div>' % (self.width, self.height, content)
                
        return content
    
    def injectScript(self):
        """ Returns a string of script to inject in to the page """

        if self.options.has_key('direction'):
            if self.options['direction'] == "":
                self.options['direction'] = 'none'
        else:
            self.options['direction'] = 'none'

        if self.options.has_key('scrollSpeed'):
            if self.options['scrollSpeed'] == "":
                self.options['scrollSpeed'] = '30'
        else:
            self.options['scrollSpeed'] = '0.5'

        if self.options.has_key('durationIsPerItem'):
            if self.options['durationIsPerItem'] == "":
                self.options['durationIsPerItem'] = '0'
        else:
            self.options['durationIsPerItem'] = '0'

        if not self.options.has_key('fitText'):
            self.options['fitText'] = '1'
        
        if int(self.options['fitText']) == 0:
            self.fitText = 'false'
            self.scaleText = 'true'
        else
            self.fitTest = 'true'
            self.scaleText = 'false'

        
        # Multiply out the duration if duration is per item.
        if not self.options['durationIsPerItem'] == '0':
            if self.itemCount > 0:
                self.duration = int(self.duration) * self.itemCount
        
        js = "<script type='text/javascript'>"
        js += "   function init() { "
        js += "       $('#text').xiboRender({ "
        js += "           type: 'ticker',"
        js += "           direction: '%s'," % self.options['direction']
        js += "           duration: %s,"; % self.duration
        js += "           durationIsPerItem: false,"
        js += "           numItems: 0,"
        js += "           width: %s," % self.width
        js += "           height: %s," % self.height
        js += "           scrollSpeed: %s," % self.options['scrollSpeed']
        js += "           fitText: %s," % self.fitText
        js += "           scaleText: %s," % self.scaleText
        js += "           scaleFactor: %s" % self.scaleFactor * 0.85
        js += "       });"
        js += "   } "
        js += "</script>"
 
        return js
    
    def browserOptions(self):
        """ Return a tuple of options for the Browser component. True/False/None. None makes no change to the
        current state. True sets to on, False sets to off. Options order is:
            Transparency,Scrollbars
        """
        return (True,False)
    
    def getContent(self):
        return []
