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

import inkex

def custom(p_options):
	return r'''Find all the ...
===+++===+++===
/* CSS part */
/* ======== */
''' + p_options.css.replace(r'\n', '\n') + r'''
===+++===+++===
// JavaScript part
//================
function getAll(ps_matchList) {
	const pArray_matchList = ps_matchList.split(',')
	return pArray_matchList
		.map(cl=>{
			const elts = Array.from(document.querySelectorAll('.'+cl))
			elts.forEach(elt=>{elt.a_matchGroup = cl})
			return elts
		})
		.flat()
}

function fixMessageDisplay() {
	const scrollCoord = (window.chrome) ? [0,0] : [document.documentElement.scrollLeft, document.documentElement.scrollTop]
	const scrollTranslateMatrix = document.documentElement.createSVGMatrix().translate(...scrollCoord)
	const screenMatrix = document.documentElement.getScreenCTM()
	const invScreenMatrix = screenMatrix.inverse()
	const matrix_trans = invScreenMatrix.multiply(scrollTranslateMatrix)
	document.querySelector('.message')?.transform.baseVal.getItem(0).setMatrix(matrix_trans)
	return 0
}

window.onscroll = fixMessageDisplay
===+++===+++===
# FuncSug part
#=============
def showNewMessageDuringSeconds(p_message, p_seconds):
	parallel exitWith branch 1 ||
		waitSeconds(p_seconds)
	||
		showNewMessageForever(p_message, 'svg', ''' + p_options.messageXShift + r''', ''' + p_options.messageYShift + r''', ''' + p_options.interline + r''')
	||
		repeat 4:
			'pause'
		calljs fixMessageDisplay()

var selector := "''' + p_options.matchList + r'''"
var elementsToFind := listToPar(calljs getAll(selector))
parallel ||
	showNewMessageDuringSeconds(`''' + p_options.welcomeMessage + r'''`, 5)
||
	while not isNovalue(elementsToFind):
		var clickedElements := parallel(for anyElement in elementsToFind, select ''' + str(p_options.matchNumber) + r'''):
			select:
				awaitClickBeep(anyElement)
			do:
				anyElement
		if allEqual(clickedElements.a_matchGroup):
			js (clickedElements):
				clickedElements.classList.add('matched')
			elementsToFind := valuesFrom(elementsToFind, 'butNotFrom', clickedElements)
		else:
			waitSeconds(1)
showNewMessageDuringSeconds(`''' + p_options.congratulationMessage + r'''`, 300)
'''

class Gamify(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--matchNumber")
		pars.add_argument("--matchList")
		pars.add_argument("--css")
		pars.add_argument("--welcomeMessage")
		pars.add_argument("--congratulationMessage")
		pars.add_argument("--messageXShift")
		pars.add_argument("--messageYShift")
		pars.add_argument("--interline")

	def effect(self):
		# custom = self.svg.metadata.findone(f"rdf:RDF/cc:Work/dc:description").text
		import gamify
		gamify.gamify(self.svg, custom(self.options), self.msg)

if __name__ == '__main__':
	Gamify().run()
