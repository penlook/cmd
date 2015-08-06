#!/usr/bin/python
#
# Pengo Project
#
# Copyright (c) 2015 Penlook Development Team
#
# --------------------------------------------------------------------
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# Authors:
#     Loi Nguyen       <loint@penlook.com>

# Application parser

from os import *
from controller import *
from view import *
from jinja2 import *
import template

class App:
	
	def __init__(self):
		pass

	def setMode(self, mode):
		self.mode = mode
		return self

	def setRoot(self, root):
		self.root = root
		self.module  = root + '/module'
		self.build   = root + '/build'
		self.service = root + '/service'
		self.buildSource = self.build + '/app'
		self.buildConfig = self.build + '/app/config'
		return self

	def expandTree(self, root):
		return listdir(root)

	def compileController(self, root, module, bundle):
		return
		targetPath = path.join(root, module, bundle, 'controller')
		destPath = path.join(self.buildSource, module, bundle, 'controller')
		if not path.isdir(destPath):
			makedirs(destPath)
		controller = Controller()
		controller.setInput(targetPath) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .setTemplate(template) \
				  .compile()

	def compileCommand(self, root, module, bundle):
		targetPath = path.join(root, module, bundle, 'command')
		destPath = path.join(self.buildSource, module, bundle, 'command')
		if not path.isdir(destPath):
			makedirs(destPath)
		#controller = Controller()
		#controller.setInput(targetPath) \
		#		  .setOutput(destPath) \
		#		  .setConfig(self.buildConfig) \
		#		  .setTemplate(template) \
		#		  .compile()

	def compileProvider(self, root, module, bundle):
		return
		targetPath = path.join(root, module, bundle, 'provider')
		destPath = path.join(self.buildSource, module, bundle, 'provider')
		if not path.isdir(destPath):
			makedirs(destPath)

	def compileResource(self, root, module, bundle):
		targetPath = path.join(root, module, bundle, 'resource', 'view')
		destPath = path.join(self.buildSource, module, bundle, 'resource', 'view')
		if not path.isdir(destPath):
			makedirs(destPath)
		template = Template('Hello {{ name }}!')
		print template.render(name='John Doe')
		return
		view = View()
		view.setInput(targetPath) \
			.setOutput(destPath) \
			.setMode(View.DEVELOPMENT) \
			.compile()
		return
		targetPath = path.join(root, module, bundle, 'resource')
		destPath = path.join(self.buildSource, module, bundle, 'resource')
		if not path.isdir(destPath):
			makedirs(destPath)

	def compileTest(self, root, module, bundle):
		targetPath = path.join(root, module, bundle, 'test')
		destPath = path.join(self.buildSource, module, bundle, 'test')
		if not path.isdir(destPath):
			makedirs(destPath)

	def compileBundle(self, root, module, bundle):
		components = self.expandTree(path.join(root, module,bundle))
		for component in components:
			if path.isdir(path.join(root, module, bundle, component)):
				if component == 'command':
					self.compileCommand(root, module, bundle)
					continue
				if component == 'controller':
					self.compileController(root, module, bundle)
					continue
				if component == 'provider':
					self.compileProvider(root, module, bundle)
					continue
				if component == 'resource':
					self.compileResource(root, module, bundle)
					continue
				if component == 'test':
					self.compileTest(root, module, bundle)
					continue

	def compileModule(self, root, module):
		bundles = self.expandTree(path.join(root, module))
		for bundle in bundles:
			if path.isdir(path.join(root, module, bundle)):
				self.compileBundle(root, module, bundle)
				return

	def parse(self):
		modules = self.expandTree(self.module)
		for module in modules:
			if path.isdir(path.join(self.module, module)):
				self.compileModule(self.module, module)