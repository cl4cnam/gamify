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
	return r'''title
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

function fixMessageDisplay1(selector) {
	const scrollCoord = (window.chrome) ? [0,0] : [document.documentElement.scrollLeft, document.documentElement.scrollTop]
	const scrollTranslateMatrix = document.documentElement.createSVGMatrix().translate(...scrollCoord)
	const screenMatrix = document.documentElement.getScreenCTM()
	const invScreenMatrix = screenMatrix.inverse()
	const matrix_trans = invScreenMatrix.multiply(scrollTranslateMatrix)
	document.querySelector(selector)?.transform.baseVal.getItem(0).setMatrix(matrix_trans)
}

function fixMessageDisplay(selector) {
	fixMessageDisplay1(selector)
	window.addEventListener('scroll', fixMessageDisplay1.bind(undefined, selector))
	return 0
}

//window.onscroll = fixMessageDisplay
''' + p_options.js.replace(r'\n', '\n') + r'''
===+++===+++===
# FuncSug part
#=============
def showNewMessageWithidDuringSeconds(p_message, p_id, p_messageXShift, p_messageYShift, p_interline, p_seconds):
	parallel exitWith branch 1 ||
		waitSeconds(p_seconds)
	||
		showNewMessageWithidForever(p_message, p_id, p_messageXShift, p_messageYShift, p_interline, 'svg')
	||
		repeat 4:
			'pause'
		var messageSelector := '#' + p_id
		calljs fixMessageDisplay(messageSelector)
def showNewMessageWithidUntilClick(p_message, p_id, p_messageXShift, p_messageYShift, p_interline):
	parallel exitWith branch 1 ||
		awaitClickBeep('#' + p_id)
	||
		showNewMessageWithidForever(p_message, p_id, p_messageXShift, p_messageYShift, p_interline, 'svg')
	||
		repeat 4:
			'pause'
		var messageSelector := '#' + p_id
		calljs fixMessageDisplay(messageSelector)

''' + p_options.funcsug.replace(r'\n', '\n')

class Gamify(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--css")
		pars.add_argument("--js")
		pars.add_argument("--funcsug")

	def effect(self):
		# custom = self.svg.metadata.findone(f"rdf:RDF/cc:Work/dc:description").text
		import gamify
		gamify.gamify(self.svg, custom(self.options), self.msg)

if __name__ == '__main__':
	Gamify().run()
