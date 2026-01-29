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
	# p_options.msg(p_options.funcsug.replace(r'\n', '\n'))
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

function getAllMatches(ps_matchList) {
	const pArray_matchList = ps_matchList.split(',')
	return {seq: pArray_matchList
		.map(cl=>{
			const elts = Array.from(document.querySelectorAll('.'+cl))
			return elts
		})}
}

function setCursorColor(color) {
	const cursor = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32'%3E%3Cpath fill='%23fed' stroke='black' d='m 0,0 20,0 12,12 0,20 -20,0 -12,-12 z'/%3E%3Ccircle fill='` + color + `' stroke='black' cx='0' cy='0' r='20'/%3E%3Cpath stroke='black' fill='none' d='m 20,0 -20,0 0,20' /%3E%3C/svg%3E") 0 0, pointer`
	document.documentElement.style.cursor = cursor
}

function getDot(color, position) {
	return `<circle cx="${position*25+20}" cy="20" r="10" fill="${color}" stroke="black">${color}</circle>`
}

function getRowOfDots(colors) {
	return '<svg id="palette" transform="translate(0 0)" width="' + colors.length*30 + '" height="40">' + colors.map((e,i)=>getDot(e, i)).join('') + '</svg>'
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
		waitSeconds(0)
		awaitClickBeep('svg')
	||
		showNewMessageWithidForever(p_message, p_id, p_messageXShift, p_messageYShift, p_interline, 'svg')
	||
		repeat 4:
			'pause'
		var messageSelector := '#' + p_id
		calljs fixMessageDisplay(messageSelector)
def colorThisDrawing(p_colors):
	parallel ||
		showNewElementIn(calljs getRowOfDots(p_colors), 'svg', 'g:svg', false, 'forever')
	||
		var color := 'white'
		calljs setCursorColor(color)

		parallel:
			sequence:
				var selector := '#palette'
				calljs fixMessageDisplay(selector)
			while true:
				var paletteEvt := awaitDomeventBeep('mousedown', '#palette')
				var palettePart := paletteEvt.target
				color := palettePart.innerHTML
				calljs setCursorColor(color)
			while true:
				var drawingEvt := awaitDomeventBeep('mousedown', 'svg')
				var drawingPart := drawingEvt.target
				drawingPart.style.fill := color
def highlightSequence(p_sequence):
	var elementsToFind := calljs getAllMatches(p_sequence)
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
		onBreak:
			js (elementsToFind):
				if (elementsToFind.num !== undefined) {
					// remove old highlighting
					const elts = elementsToFind.seq[elementsToFind.num]
					elts.forEach(elt=>{elt.classList.remove('highlight')})
				}
def matchItems(p_numberPerMatch, p_matchList):
	var elementsToFind := listToPar(calljs getAll(p_matchList))
	var remainingElements := elementsToFind
	while not isNovalue(remainingElements):
		var clickedElements := parallel(for anyElement in remainingElements, select p_numberPerMatch):
			select:
				awaitClickBeep(anyElement)
			do:
				addCssClassTo('chosen', anyElement)
				anyElement
		if allEqual(clickedElements.a_matchGroup):
			addCssClassTo('matched', clickedElements)
			remainingElements := valuesFrom(remainingElements, 'butNotFrom', clickedElements)
		else:
			waitSeconds(1)
		delCssClassFrom('chosen', clickedElements)
	# awaitForever()
	waitSeconds(1)
	js (elementsToFind):
		elementsToFind.classList.remove('matched')

''' + p_options.funcsug.replace(r'\n', '\n').replace('    ', '\t')

class Gamify(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--tab2")
		pars.add_argument("--tab3")
		pars.add_argument("--css")
		pars.add_argument("--js")
		pars.add_argument("--funcsug")

	def effect(self):
		# custom = self.svg.metadata.findone(f"rdf:RDF/cc:Work/dc:description").text
		import gamify
		# self.options.msg = self.msg
		gamify.gamify(self.svg, custom(self.options), self.msg)

if __name__ == '__main__':
	Gamify().run()
