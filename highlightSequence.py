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
	return {seq: pArray_matchList
		.map(cl=>{
			const elts = Array.from(document.querySelectorAll('.'+cl))
			return elts
		})}
}

function highlight(list, direction) {
	if (list.num === undefined) {
		if (direction == 1) list.num = -1
		else return
	} else {
		// remove old highlighting
		const elts = list.seq[list.num]
		elts.forEach(elt=>{elt.classList.remove('highlight')})
	}
	// go in direction
	list.num += direction
	list.num %= list.seq.length
	list.num += list.seq.length
	list.num %= list.seq.length
	// add highlighting
	const elts = list.seq[list.num]
	elts.forEach(elt=>{elt.classList.add('highlight')})
}

===+++===+++===
# FuncSug part
#=============
var selector := "''' + p_options.matchList + r'''"
var elementsToFind := calljs getAll(selector)
parallel ||
	var direction := 1
	while true:
		awaitClickBeep('svg')
		calljs highlight(elementsToFind, direction)
||
	var direction := 1
	while true:
		var evt := awaitDomeventBeep('keydown', 'svg')
		if evt.key = 'ArrowRight':
			calljs highlight(elementsToFind, direction)
||
	var direction := -1
	while true:
		var evt := awaitDomeventBeep('keydown', 'svg')
		if evt.key = 'Backspace' or evt.key = 'ArrowLeft':
			calljs highlight(elementsToFind, direction)
'''

class Gamify(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--matchList")
		pars.add_argument("--css")

	def effect(self):
		# custom = self.svg.metadata.findone(f"rdf:RDF/cc:Work/dc:description").text
		import gamify
		gamify.gamify(self.svg, custom(self.options), self.msg)

if __name__ == '__main__':
	Gamify().run()
