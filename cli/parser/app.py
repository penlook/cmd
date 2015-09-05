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
from compiler import *
from generator import *
from view import *
import template
from volt import *
import shutil

class App:

	def __init__(self):
		self.listFiles   = []
		self.viewStack   = []
		self.listInclude = {}
		self.listCommand = []

	def setMode(self, mode):
		self.mode = mode
		return self

	def setRoot(self, root):
		self.root = root
		self.module  = root + '/src'
		self.build   = root + '/gen'
		self.container = self.build + '/container'
		self.excutable = self.build + '/excutable'
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
		print '    controller'
		targetPath = path.join(root, module, bundle, 'controller')
		destPath = path.join(self.container, module, bundle, 'controller')
		if not path.isdir(destPath):
			makedirs(destPath)
		compiler = Compiler('controller')
		compiler  .setInput(targetPath) \
		 		  .setNamespace([module, bundle, 'controller']) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .setTemplate(template) \
				  .compile()
		# Get all variables in actions
		self.viewData   = compiler.viewData
		self.listInclude = compiler.includeAll

	def compileCommand(self, root, module, bundle):
		print '     command'
		targetPath = path.join(root, module, bundle, 'command')
		destPath = path.join(self.container, module, bundle, 'command')
		if not path.isdir(destPath):
			makedirs(destPath)
		compiler = Compiler('command')
		compiler  .setInput(targetPath) \
				  .setNamespace([module, bundle, 'command']) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .compile()
		for cmdFile in compiler.getListFile():
			commandClass = '::'.join([module, bundle, 'command', cmdFile]).split('.cpp')[0]
			self.listCommand.append(commandClass)

	def compileProvider(self, root, module, bundle):
		# Compile entity model
		targetPath = path.join(root, module, bundle, 'provider', 'entity')
		destPath = path.join(self.container, module, bundle, 'provider', 'entity')
		if not path.isdir(destPath):
			makedirs(destPath)
		compiler = Compiler('model')
		compiler  .setInput(targetPath) \
				  .setNamespace([module, bundle, 'entity']) \
				  .setOutput(destPath) \
				  .setConfig(self.buildConfig) \
				  .compile()

	def compileResource(self, root, module, bundle):
		return
		# Compile volt template
		viewTargetPath = path.join(root, module, bundle, 'resource', 'view')
		viewDestPath = path.join(self.container, module, bundle, 'resource', 'view')
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
			controllerName = componentPath[0]
			viewHeader = '#include "view/view.h"\n'
			if self.listInclude.has_key(controllerName):
				for include in self.listInclude[controllerName]:
					viewHeader += include + '\n'
			funcName = module + '_' + bundle  + '_' + '_'.join(componentPath)
			self.viewStack.append(funcName);
			if len(componentPath) == 2:
				if hasattr(self, 'viewData'):
					# Controller view
					if self.viewData.has_key(componentPath[0]):
						# Action view
						if self.viewData[componentPath[0]].has_key(componentPath[1]):
							volt.setData({
								"variables" : self.viewData[componentPath[0]][componentPath[1]],
								"viewHeader" : viewHeader,
								"funcName": funcName
							})
							volt.compile(templateFile, destCompileFile + ".cpp.html")
							os.remove(destCompileFile + ".cpp.html")
		#targetPath = path.join(root, module, bundle, 'resource')
		#destPath = path.join(self.container, module, bundle, 'resource')
		#if not path.isdir(destPath):
		#	makedirs(destPath)

	def compileTest(self, root, module, bundle):
		targetPath = path.join(root, module, bundle, 'test')
		destPath = path.join(self.container, module, bundle, 'test')
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
					#self.compileController(root, module, bundle)
					continue
				if component == 'provider':
					#self.compileProvider(root, module, bundle)
					continue
				if component == 'resource':
					#self.compileResource(root, module, bundle)
					continue
				if component == 'test':
					#self.compileTest(root, module, bundle)
					continue

	def compileModule(self, root, module):
		bundles = self.expandTree(path.join(root, module))
		for bundle in bundles:
			if path.isdir(path.join(root, module, bundle)):
				print '  ', bundle
				self.compileBundle(root, module, bundle)

	def generateViewHeader(self):
		viewHeaderDir = self.container + '/view'
		if not path.isdir(viewHeaderDir):
			makedirs(viewHeaderDir)
		volt = Volt()
		volt.generateHeader(viewHeaderDir, self.viewStack)

	def generateMain(self):
		cliDir = self.excutable + '/cli'
		serverDir = self.excutable + '/server'
		if not path.isdir(cliDir):
			makedirs(cliDir)
		if not path.isdir(serverDir):
			makedirs(serverDir)
		generator = Generator()
		generator.setOutput(cliDir)\
				 .setListCommand(self.listCommand)\
				 .generateCli()\
				 .setOutput(serverDir)\
				 .generateServer()

	def generateMakefile(self):
		genMakefile = self.root
		generator = Generator()
		generator.setOutput(self.root)\
				 .generateAppMakefile()\
				 .setOutput(self.build)\
				 .generateGenMakefile()

	def compileSource(self):
		print 'Compiling ..'
		modules = self.expandTree(self.module)
		for module in modules:
			if module.startswith("_cpp_"):
				if path.isdir(path.join(self.module, module)):
					if path.isdir(path.join(self.container, module)):
						shutil.rmtree(path.join(self.container, module))
					print module
					self.compileModule(self.module, module)
		self.generateViewHeader()

	def compileConfig(self):
		pass

	def parse(self):
		self.compileSource()
		self.generateMain()
		self.generateMakefile()