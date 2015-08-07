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

# Controller parser

import os
import sys
import pprint
import hashlib
from pattern import *
import pprint

def tab(times):
	tabContent = '\n'
	for i in range(0, times):
		tabContent += '\t'
	return tabContent

class ClassCompiler:

	def __init__(self, typeName):
		self.typeName =  typeName
		self.controller = False
		self.command = False
		self.model = False
		self.initClassParser()
		if typeName == 'controller':
			self.controller = True
			self.initControllerParser()
		if typeName == 'command':
			self.command = True
			self.initCommandParser()
		if typeName == 'model':
			self.model = True
			self.initModelParser()
	
	def initClassParser(self):
		self.commentFlag = False
		self.bracketFlag = 0
		self.methodStack = {}
		self.annotationStack = {}
		self.lineStack = []
		self.stackPublic = []
		self.stackPrivate = []
		self.stackProtected = []
		self.stackNonAccessModifier = []
		self.methodBlockContent = {}
		self.annotationInfo = {}
		self.currentClass = None
		self.currentClassFull = None
		self.currentMethod = None

	def initCommandParser(self):
		pass

	def initModelParser(self):
		pass

	def initControllerParser(self):
		self.defaultAnnotation = {
			'@Route': None,
			'@Method': '*',
			'@Type': 'HTML'
		}
		self.viewData = {}
		self.isAction = False

	def setInput(self, targetDir):
		self.Input = targetDir
		return self

	def setOutput(self, destDir):
		self.Output = destDir
		if not os.path.isdir(self.Output):
			os.makedirs(self.Output)
		return self

	def setTemplate(self, templateContext):
		self.Template = templateContext
		return self

	def setConfig(self, configDir):
		self.Config = configDir
		return self

	def getViewData(self):
		return self.viewData

	def parseSourceFile(self, sourcePath):
		pass

	def parseController(self, cppPath):
		self.initControllerParser()
		annotationStorage = {}
		self.annotationStack = {}
		# Pattern recognition
		pattern = Pattern()
		pattern.setContext(self)
		# Compile file
		with open(cppPath, "r") as lines :
			for line in lines:
				line = line.strip()
				if len(line) > 0:
					self.line = line
					self.lineStack.append(line)
					if pattern.isComment():
						continue
					if pattern.isHeader():
						self.headerContent += self.line + "\n"
						continue
					if pattern.isAnnotation():
						annotationArr = self.line.split(' ')
						annotationName = annotationArr[0].strip()
						annotationValue = ' '.join(annotationArr[1:])
						if annotationName == '@Route':
							self.isAction = True
						self.annotationStack[annotationName] = annotationValue
						continue
					if pattern.isMethod() and self.bracketFlag == 0:
						# Default
						method_without_am = self.line
						am = False
						if pattern.isPublic():
							method_without_am = self.line.split('public')[1].strip()
							method_without_am = method_without_am
							if self.isAction:
								method_without_am = 'void '+ method_without_am
							self.stackPublic.append(method_without_am)
							if self.isAction:
								# Method as Action
								action_without_am = method_without_am.split('(')[0] + "(ActionArgumentList)"
								self.stackPublic.append(action_without_am)
							am = True
						if pattern.isPrivate():
							method_without_am = self.line.split('private')[1].strip()
							method_without_am = method_without_am
							if self.isAction:
								method_without_am = 'void '+ method_without_am
							self.stackPrivate.append(method_without_am)
							if self.isAction:
								# Method as Action
								action_without_am = method_without_am.split('(')[0] + "(ActionArgumentList)"
								self.stackPrivate.append(action_without_am)
							am = True
						if pattern.isProtected():
							method_without_am = self.line.split('protected')[1].strip()
							method_without_am = method_without_am
							if self.isAction:
								method_without_am = 'void '+ method_without_am
							self.stackProtected.append(method_without_am)
							if self.isAction:
								# Method as Action
								action_without_am = method_without_am.split('(')[0] + "(ActionArgumentList)"
								self.stackPrivate.append(action_without_am)
							am = True
						if am is False:
							method_without_am = method_without_am
							self.stackNonAccessModifier.append(method_without_am)

						#print method_without_am
						indexL = method_without_am.index('(')
						indexR = indexL
						while indexR > 0:
							if method_without_am[indexR] == ' ':
								break
							indexR = indexR - 1
						currentMethod = method_without_am[indexR : indexL]
						self.currentMethod = currentMethod.strip()
						#print currentMethod
						self.methodStack[self.currentMethod] = {}
						if self.isAction:
							self.methodStack[self.currentMethod]["Header"] = "void " + className + "::" + currentMethod.strip() + '(ActionArgumentList args)'
							self.viewData[self.currentClass.lower()][self.currentMethod.lower()] = []
						else:
							self.methodStack[self.currentMethod]["Header"] = method_without_am[0 : indexR] + " " + className + "::" + currentMethod.strip() + method_without_am[indexL:]
						self.methodStack[self.currentMethod]["Block"] = ''
						indexL = method_without_am.index('(')
						indexR = method_without_am.index(')')
						#self.methodStack[self.currentMethod]["Header"] += method_without_am[indexL : indexR + 1]
						arguments = method_without_am[indexL + 1 : indexR]
						argumentPairs = arguments.split(',')
						argumentList = []
						if len(argumentPairs) > 0:
							for argumentPair in argumentPairs:
								variableCom  = argumentPair.split(' ')
								variableName = variableCom[-1].strip()
								variableType = ''
								variableType = variableType.join(variableCom[0:len(variableCom) - 1]).strip()
								if (len(variableType) > 0) and (len(variableName) > 0):
									argumentList.append([variableType, variableName])
						self.methodStack[self.currentMethod]["Argument"] = argumentList
						declare = ''
						#print argumentList
						if self.isAction:
							for argument in argumentList:
								#declare += argument[0] + ' ' + argument[1] + ' = args.front()->getVariable();\nargs.pop(); \n'
								#declare += 'ActionArgument *arg' + argument[1] +' = args.front();\nargs.pop();\n'
								#declare += 'cout << arg' + argument[1] + '->getVariable();\n'
								#self.cppContent  += 'cout << args.pop();\n'
								#declare += argument[0] + ' ' + argument[1] +' = args.front()->getVariable();\nargs.pop();\n';
								pass
						self.methodStack[self.currentMethod]['ArgDeclaration'] = declare
						if len(self.annotationStack) > 0:
							self.annotationStack['@Argument'] = argumentList
							self.annotationInfo[self.currentClass]['Method'].append(
								{'Name': currentMethod, '@': self.annotationStack }
							)
							#print self.annotationInfo
						self.annotationStack = {}
						continue
					if pattern.isProperty() and self.bracketFlag == 0:
						am = False
						property_without_am = ' '
						if pattern.isPublic():
							am = True
							property_without_am = self.line.split('public')[1]
							self.stackPublic.append(property_without_am.strip())
						if pattern.isPrivate():
							am = True
							property_without_am = self.line.split('private')[1]
							self.stackPrivate.append(property_without_am.strip())
						if pattern.isProtected():
							am = True
							property_without_am = self.line.split('protected')[1]
							self.stackProtected.append(property_without_am.strip())
						if am is False:
							self.stackNonAccessModifier.append(property_without_am.strip())
						continue
					if pattern.isClass():
						class_without_bracket = self.line
						if pattern.isEndWithBracket():
							class_without_bracket = self.line.split('{')[0]
						className = class_without_bracket.split(' ')[1]
						self.currentClass = className
						self.currentClassFull = class_without_bracket
						self.annotationInfo[self.currentClass] = {'@': self.annotationStack, 'Method': []}
						self.annotationStack = {}
						self.viewData[self.currentClass.lower()] = {}
						continue
					if pattern.isTemplateVariable():
						equal = self.line.index("=")
						variable = self.line[:equal]
						value = self.line[equal:]
						bracketStart = variable.index("<")
						bracketStop  = variable.index(">")
						variableName = variable[:bracketStart]
						variableType = variable[bracketStart + 1 : bracketStop]
						self.line = variableType + " " + variableName + ' ' + value + '\n';
						self.line += 'this->getView()->getData()->set<' + variableType + '>("' + variableName + '", ' + variableName + ');'
						self.viewData[self.currentClass.lower()][self.currentMethod.lower()].append({
							'Type': variableType,
							'Name': variableName
						})
						#self.viewData[self.currentClass][self.currentMethod] += variableType + ' ' +variableName + ' = view->getData()->get<' + variableType + '>("' + variableName + '");\n'
					if pattern.isMethodStart():
						self.bracketFlag = 1
						continue
					if pattern.isMethodStop():
						self.bracketFlag = 0
						self.isAction = False
						continue
					if self.currentMethod is not None:
						for i in range(0, len(self.line)):
							if self.line[i] == '{':
								self.bracketFlag += 1
							if self.line[i] == '}':
								self.bracketFlag -= 1
						if self.bracketFlag > 0:
							self.methodStack[self.currentMethod]["Block"] += self.line + '\n'
						continue
		if self.currentClass is None:
			print 'Controller class does not exist !'
			exit()

	def generateHeader(self):
		self.headerContent += 'namespace app {\nnamespace ' + self.typeName + ' {\n'
		self.headerContent += self.currentClassFull + "\n{\n"
		if len(self.stackPublic) > 0:
			self.headerContent += '\tpublic:\n'
		for publicItem in self.stackPublic:
			self.headerContent += '\t\t' + publicItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ";"
			self.headerContent += '\n'
		if len(self.stackPrivate) > 0:
			self.headerContent += '\tprivate:\n'
		for privateItem in self.stackPrivate:
			self.headerContent += '\t\t' + privateItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ';'
			self.headerContent += '\n'
		if len(self.stackProtected) > 0:
			self.headerContent += '\tprotected:\n'
		for protectedItem in self.stackProtected:
			self.headerContent += '\t\t' + protectedItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ';'
			self.headerContent += '\n'
		for protectedItem in self.stackNonAccessModifier:
			self.headerContent += '\t' + protectedItem.strip()
			if not self.headerContent.endswith(';'):
				self.headerContent += ';'
			self.headerContent += '\n'
		self.headerContent += '};\n'
		self.headerContent += "}\n}"

	def generateSource(self):
		self.cppContent += 'namespace app {\nnamespace ' + self.typeName +' {\n'
		for methodName in self.methodStack:
			self.cppContent += self.methodStack[methodName]['Header'].rstrip('\n') + '\n'
			self.cppContent += '{\n'
			self.cppContent += self.methodStack[methodName]['ArgDeclaration']
			self.cppContent += self.methodStack[methodName]['Block'].rstrip('\n') + '\n'
			self.cppContent += '}\n'
		self.cppContent += '}\n}'

	def compileFile(self, filePath):
		fileName = filePath.split(".")[0]
		self.className = fileName.split("/")[-1]
		cppPath	   = self.Input + "/" + fileName + ".cpp"
		destHeaderPath = self.Output + "/" + fileName + ".h"
		destCppPath = self.Output + "/" + fileName + ".cpp"
		# Include header in source file
		self.headerContent = ''
		self.cppContent = '#include "'+ self.className + '.h"\n'
		self.parseController(cppPath)
		self.generateHeader()
		self.generateSource()
		# Prepare to write
		header = open(destHeaderPath, 'w')
		cpp = open(destCppPath, 'w')
		# Write content to file
		header.write(self.headerContent)
		header.close()
		cpp.write(self.cppContent)
		cpp.close()

	def mergeAnnotation(self):
		annotationList = []
		for className in self.annotationInfo:
			classAnnotation = self.annotationInfo[className]['@']
			for methodInfo in self.annotationInfo[className]['Method']:
				# Override class annotation
				for defaultAnnotation in classAnnotation:
					if defaultAnnotation not in methodInfo['@']:
						methodInfo['@'][defaultAnnotation] = classAnnotation[defaultAnnotation]
				# If really missing annotation, then using default annotation
				for defaultAnnotation in self.defaultAnnotation:
					if defaultAnnotation not in methodInfo['@']:
						methodInfo['@'][defaultAnnotation] = self.defaultAnnotation[defaultAnnotation]
				# Add controller - action
				methodInfo['@']['@Controller'] = className
				methodInfo['@']['@Action'] = methodInfo['Name']
				annotationList.append(methodInfo['@'])
		return annotationList

	def renderString(self, template, data):
		content = ''
		start = 0
		end = -1
		for match in re.finditer(r"\{\{[a-zA-Z0-9_\s]+\}\}", template):
			end = match.start()
			if start < end:
				content += template[start:end]
			start = end + 1
			var_block = template[match.start():match.end()]
			var = re.split("\s+", var_block)[1]
			if var in data:
				content += data[var]
			start = match.end()
		content += template[start:]
		content = content.replace('"', '\"')
		return content

	def generateControllerActionMapping(self):
		controllesH = os.path.abspath(self.Output + '/../main/controllers.h')
		controllers = open(controllesH, 'w')
		controllersTemplate = """
// AUTO GENERATED
#include <map>
#include <vector>
#include <functional>
#include "view/view.h"
#include <app/controller.h>
{{ headers }}
namespace app {
	ListController getControllers() {
		ListController controllers;{{ controllers }}
		return controllers;
	}
	template <typename T>
	void convertController(T *targetController, Controller *childController)
	{
		childController ->setHash(targetController->getHash())
						->setView(new View);
	}
	void callbackAction(Controller *controller)
	{
		ListController controllers = getControllers();
		Action *action = controller->getAction();
		string actionFlag = controller->getName() + "-" + action->getName();
		ActionArgumentList args = action->getArguments();{{ actions }}
	}
}"""
		controllerList = ''
		actionList = ''
		headerList = ''
		hashMd5 = hashlib.md5()
		#pprint.pprint(self.annotationInfo)
		for className in self.annotationInfo:
			headerList += '#include "controller/' + className.lower() + '.h"\n'
			controllerName = className.lower() + 'Controller'
			controllerList += tab(2) + 'controller::' + className + ' *' + controllerName +' = new controller::' + className + ';'
			controllerList += tab(2) + 'controllers["' + className + '"] = ' + controllerName + ';'
			controllerList += tab(2) + controllerName + tab(4) + '->setName("' + className + '")'
			for methodInfo in self.annotationInfo[className]['Method']:
				actionName = methodInfo['Name'].strip()
				actionList += tab(2) + 'if (actionFlag == "' + className + '-' + actionName + '") { controller::' + className + ' *' + className.lower() + ' = (controller::' + className +'*) controllers[controller->getName()];convertController(controller, ' + className.lower() + ');' + className.lower() +'->'+ actionName + '(args);return;}'
				hashMd5.update(className + '-' + actionName)
				hashAction = hashMd5.hexdigest()
				controllerList += tab(4) + '->addAction(' + tab(5) +'(new Action)'
				controllerList += tab(6) + '->setName("' + actionName +'")'
				templateFile = os.path.abspath(os.getcwd() + "/../../module/home/resource/view/" + className.lower() + '/' + actionName.lower() + '.html')
				if os.path.isfile(templateFile):
					controllerList += tab(6) + '->setViewCallback(view::' + className.lower() + '_' + actionName.lower() + ')'
				#for print methodInfo['@']['@Method']
				controllerList += tab(6) + '->setHash("' + hashAction + '")'
				if len(methodInfo['@']['@Argument']) > 0:
					for argumentPair in methodInfo['@']['@Argument']:
						controllerList += tab(6) + '->addArgument(new ActionArgument("' + argumentPair[0] + '","' + argumentPair[1] + '"))'
				controllerList += tab(4) + ')'
			controllerList += ';'

		controllersContent = self.renderString(controllersTemplate, {
			'controllers' : controllerList,
			'actions' : actionList,
			'headers': headerList
		})
		controllers.write(controllersContent)

	def generateNginxConfig(self):
		annotationList = self.mergeAnnotation()
		#pprint.pprint(annotationList)
		location = ""
		configContent = """
location / {
	app 123456789;
}"""
		configContent = self.Template.nginx_config.replace('{{ app }}', configContent)
		app_config = self.Config + '/app.conf'
		nginx = open(app_config, 'w')
		nginx.write(configContent)

	def compile(self):
		# List all class files from input directory
		classFiles = os.listdir(self.Input)
		for classFile in classFiles:
			if classFile.endswith('.cpp'):
				# Compile cpp file
				self.compileFile(classFile)
		#self.generateNginxConfig()
		#self.generateControllerActionMapping()