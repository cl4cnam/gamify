#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2025 Claude Lion
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Description of this extension
"""

from urllib.parse import quote

def getContent(ps_path):
	with open(ps_path) as f:
		return f.read()

def addScript(p_svg, ps_identity, ps_content, pb_funcsug, pb_file=True, msg=False):
	import lxml
	xpathSearch = "//svg:*[@identity = '" + ps_identity + "' ]"
	scrs = p_svg.xpath(xpathSearch)
	scr = scrs[0] if scrs else lxml.etree.Element('style') if ps_identity == 'customCss' else lxml.etree.Element('script')
	suffix = '.fg' if pb_funcsug else '.js'
	scr.text = getContent('FuncSug/' + ps_identity + suffix) if pb_file else ps_content
	scr.set('identity', ps_identity)
	if pb_funcsug:
		scr.set('type', 'application/funcsug')
	p_svg.add(scr)

def gamify(p_svg, ps_custom, msg):
		customTitle,customCss, customJs, customFg = ps_custom.split('===+++===+++===')
		customTitle = customTitle.strip()
		
		addScript(p_svg, 'customCss', customCss, False, False)
		addScript(p_svg, 'libStd', '', True)
		addScript(p_svg, 'libDOM', '', True)
		addScript(p_svg, 'libMove', '', True)
		addScript(p_svg, 'libDOMSVG', '', True)
		addScript(p_svg, 'customFg', customFg, True, False)
		addScript(p_svg, 'customJs', customJs, False, False)
		addScript(p_svg, 'parser', '', False)
		addScript(p_svg, 'parserPy', '', False)
		addScript(p_svg, 'interpreter', '', False)
		addScript(p_svg, 'DOMloader', '', False)
		
