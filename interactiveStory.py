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
	import re
	inputText = '\n' + p_options.story.replace('\\n', '\n').replace('    ', '\t')
	inputText = re.sub(r'\n(\t*)!: (.*)(?=\n)',r'\n\1showMessage("\2")', inputText)
	inputText = re.sub(r'\n(\t*)!(.*): (.*)(?=\n)',r'\n\1showTalk("\3", "#\2")', inputText)
	# ~ inputText = re.sub(r'\n(\t*)\?: (.*)(?=\n)',r'\n\1showMessage("\2")\n\1parallel(select 1) ||', inputText)
	inputText = re.sub(r'\n(\t*)\?: (.*)(?=\n)',r'\n\1parallel(select 1) ||\n\1||=========================\n\1\tshowMessage("\2")\n\1\tawaitForever()\n\1...-------\n\1\t"dummy"', inputText)
	# ~ inputText = re.sub(r'\n(\t*)\?(.*): (.*)(?=\n)',r'\n\1showTalk("\3", "#\2")\n\1parallel(select 1) ||', inputText)
	inputText = re.sub(r'\n(\t*)\?(.*): (.*)(?=\n)',r'\n\1parallel(select 1) ||\n\1||=========================\n\1\tshowTalk("\3", "#\2")\n\1\tawaitForever()\n\1...-------\n\1\t"dummy"', inputText)
	inputText = re.sub(r'\n(\t*)-> (.*)(?=\n)',r'\n\1||=========================\n\1\tWAIT_FOR_CHOICE("\2")\n\1...-------', inputText)
	inputText = re.sub(r'\n(\t*)->\* (.*)(?=\n)',r'\n\1||=========================\n\1\t\2\n\1...-------', inputText)
	# ~ p_options.msg(inputText)
	return r'''Find all the ...
===+++===+++===
/* CSS part */
/* ======== */
''' + p_options.css.replace(r'\n', '\n') + r'''
===+++===+++===
// JavaScript part
//================
function getAll(ps_selector) {
	return document.querySelectorAll(ps_selector)
}

===+++===+++===
# FuncSug part
#=============
def hide(p_elt):
	js (p_elt):
		document.querySelector(p_elt).style.display = 'none'
def show(p_elt):
	js (p_elt):
		document.querySelector(p_elt).style.display = 'inline'
def switch(p_elt1, p_elt2):
	hide(p_elt1)
	show(p_elt2)

var choiceCounter := js([], `return {num: 1}`)
def resetChoiceCounter():
	js (choiceCounter):
		choiceCounter.num = 1

def showNewMessageUntilClick(p_message, p_id, p_class, p_num):
	parallel exitWith branch 1 ||
		waitSeconds(0)
		awaitClickBeep('#' + p_id)
	||
		showNewMessageWithidForever(p_message, p_id, 20, p_num*50, 30, 'svg/' + p_class)
	||
		if p_class = 'choice':
			'workaroundString'
			var elt := getElement('#choice' + p_num)
			js (elt):
				elt.firstElementChild.setAttribute('rx', 0)
				elt.firstElementChild.setAttribute('ry', 0)
		awaitForever()

def showMessage(p_message):
	resetChoiceCounter()
	showNewMessageUntilClick(p_message, 'theMessage', 'simple', 0)

def showTalk(p_message, p_character):
	resetChoiceCounter()
	parallel exitWith branch 1 ||
		showNewMessageUntilClick(p_message, 'theMessage', 'talk', 0)
	||
		showElementForever(getElement(p_character))

def WAIT_FOR_CHOICE(p_choice):
	var num := js (choiceCounter):
		choiceCounter.num += 1
		return choiceCounter.num
	showNewMessageUntilClick(p_choice, 'choice' + num, 'choice', num)

#showTalk(`Temporary?`, '#char1')
#parallel(select 1) ||
#||=========
#	WAIT_FOR_CHOICE('Yes')
#...---
#	showMessage(`Ah!`)
#||=========
#	WAIT_FOR_CHOICE('No')
#...---
#	showMessage(`Oh!`)
''' + inputText

class Gamify(inkex.EffectExtension):
	def add_arguments(self, pars):
		pars.add_argument("--tab")
		pars.add_argument("--story")
		pars.add_argument("--css")
		pars.add_argument("--messageXShift")
		pars.add_argument("--messageYShift")
		pars.add_argument("--interline")

	def effect(self):
		# custom = self.svg.metadata.findone(f"rdf:RDF/cc:Work/dc:description").text
		import gamify
		self.options.msg = self.msg
		gamify.gamify(self.svg, custom(self.options), self.msg)

if __name__ == '__main__':
	Gamify().run()
