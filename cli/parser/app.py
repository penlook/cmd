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
from classCompiler import *
from view import *
import template
from volt import *

class App:

	def __init__(self):
		self.listFiles = []
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

	def expandTreeRecursive(self, root):
		if path.isdir(root):
			listFiles = self.expandTree(root)
			for file in listFiles:
				if path.isdir(path.join(root, file)):
					self.expandTreeRecursive(path.join(root, file))
				if path.isfile(path.join(root, file)):
					self.listFiles += [path.join(root, file)]

	def compileController(self, root, module, bundle):
		targetPath = path.join(root, module, bundle, 'controller')
		destPath = path.join(self.buildSource, module, bundle, 'controller')
		if not path.isdir(destPath):
			makedirs(destPath)
		compiler = ClassCompiler('controller')
		compiler  .setInput(targetPath) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .setTemplate(template) \
				  .compile()
		# Get all variables in actions
		self.viewData = compiler.viewData

	def compileCommand(self, root, module, bundle):
		targetPath = path.join(root, module, bundle, 'command')
		destPath = path.join(self.buildSource, module, bundle, 'command')
		if not path.isdir(destPath):
			makedirs(destPath)
		compiler = ClassCompiler('command')
		compiler  .setInput(targetPath) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .compile()
		#controller = Controller()
		#controller.setInput(targetPath) \
		#		  .setOutput(destPath) \
		#		  .setConfig(self.buildConfig) \
		#		  .setTemplate(template) \
		#		  .compile()

	def compileProvider(self, root, module, bundle):
		# Compile entity model
		targetPath = path.join(root, module, bundle, 'provider', 'entity')
		destPath = path.join(self.buildSource, module, bundle, 'provider', 'entity')
		if not path.isdir(destPath):
			makedirs(destPath)
		compiler = ClassCompiler('model')
		compiler  .setInput(targetPath) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .compile()

	def compileResource(self, root, module, bundle):
		# Compile volt template
		viewTargetPath = path.join(root, module, bundle, 'resource', 'view')
		viewDestPath = path.join(self.buildSource, module, bundle, 'resource', 'view')
		if not path.isdir(viewDestPath):
			makedirs(viewDestPath)
		self.listFiles = []
		volt = Volt()
		templateFiles = self.expandTreeRecursive(viewTargetPath)
		for templateFile in self.listFiles:
			if not path.isdir(path.dirname(viewDestPath + templateFile[len(viewTargetPath):])):
				makedirs(path.dirname(viewDestPath + templateFile[len(viewTargetPath):]))
			destCompileFile = viewDestPath + templateFile[len(viewTargetPath):]
			destCompileFile = destCompileFile.split(".")[0]
			componentPath = templateFile[len(viewTargetPath):].split(".html")[0].split('/')[1:]
			if len(componentPath) == 2:
				# Controller view
				if self.viewData.has_key(componentPath[0]):
					# Action view
					if self.viewData[componentPath[0]].has_key(componentPath[1]):
						volt.setData(self.viewData[componentPath[0]][componentPath[1]])
						volt.compile(templateFile, destCompileFile + ".cpp.html")
		#targetPath = path.join(root, module, bundle, 'resource')
		#destPath = path.join(self.buildSource, module, bundle, 'resource')
		#if not path.isdir(destPath):
		#	makedirs(destPath)

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