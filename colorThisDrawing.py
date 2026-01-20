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
	return r'''Color this Drawing
===+++===+++===
/* CSS part */
/* ======== */
#palette {
	position: fixed; top: 0; left: 0; display: inline-table; z-index: 100;
}
===+++===+++===
// JavaScript part
//================
const ALL_COLORS = ['purple', 'magenta', 'red', 'orange', 'yellow', 'lime', 'green', 'cyan', 'blue', 'brown', 'white', 'silver', 'black']

function setCursorColor(color) {
	const cursor = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32'%3E%3Cpath fill='%23fed' stroke='black' d='m 0,0 20,0 12,12 0,20 -20,0 -12,-12 z'/%3E%3Ccircle fill='` + color + `' stroke='black' cx='0' cy='0' r='20'/%3E%3Cpath stroke='black' fill='none' d='m 20,0 -20,0 0,20' /%3E%3C/svg%3E") 0 0, pointer`
	document.documentElement.style.cursor = cursor
}

function getDot(color, position) {
	return `<circle cx="${position*25+20}" cy="20" r="10" fill="${color}" stroke="black">${color}</circle>`
}

function getRowOfDots() {
	return '<svg id="palette" transform="translate(0 0)" width="' + ALL_COLORS.length*30 + '" height="40">' + ALL_COLORS.map((e,i)=>getDot(e, i)).join('') + '</svg>'
}

function fixPaletteDisplay() {
	const startMatrix = document.documentElement.getScreenCTM()
	const matrix_trans = startMatrix.inverse()
	document.getElementById('palette').transform.baseVal.getItem(0).setMatrix(matrix_trans)
}

window.onscroll = function(evt) {
	const scrollCoord = (window.chrome) ? [0,0] : [document.documentElement.scrollLeft, document.documentElement.scrollTop]
	const translateMatrix = document.documentElement.createSVGMatrix().translate(...scrollCoord)
	const startMatrix = document.documentElement.getScreenCTM()
	const matrix_trans = startMatrix.inverse().multiply(translateMatrix)
	document.getElementById('palette').transform.baseVal.getItem(0).setMatrix(matrix_trans)
}

===+++===+++===
# FuncSug part
#=============
parallel ||
	showNewElementIn(calljs getRowOfDots(), 'svg', 'g:svg', false, 'forever')
||
	var color := 'white'
	calljs setCursorColor(color)

	parallel:
		sequence:
			calljs fixPaletteDisplay()
		while true:
			var paletteEvt := awaitDomeventBeep('mousedown', '#palette')
			var palettePart := paletteEvt.target
			color := palettePart.innerHTML
			calljs setCursorColor(color)
		while true:
			var drawingEvt := awaitDomeventBeep('mousedown', 'svg')
			var drawingPart := drawingEvt.target
			drawingPart.style.fill := color
'''

class Gamify(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")

	def effect(self):
		# custom = self.svg.metadata.findone(f"rdf:RDF/cc:Work/dc:description").text
		import gamify
		gamify.gamify(self.svg, custom(self.options), self.msg)

if __name__ == '__main__':
	Gamify().run()
