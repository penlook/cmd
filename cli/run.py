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

import sys
from os import *
import argparse
from parser import *
import proxy
import time

#$ pen run
#$ pen run app
class Run(argparse.Action):
	
	def prepare(self):
		self.cwd += '/gen/_development'
		chdir(self.cwd)
		# Clean up system
		system("sync && echo 3 > /proc/sys/vm/drop_caches")
		system("pkill pendev && service nginx stop")
		system("fuser -k 80/tcp")

	def compileView(self):
		print 'Template - Starting complie ...'
		view = View()
		view.setInput(self.root + "/module/home/user/resource/view") \
			.setOutput(self.root + "/build/app/view") \
			.setMode(View.DEVELOPMENT) \
			.compile()
		print 'Template - Done.'

	def compileController(self):
		print 'Controller - Starting complie ...'
		controller = Controller()
		controller.setInput(self.root + "/module/home/user/controller") \
				  .setOutput(self.root + "/build/app/controller") \
				  .setConfig(self.root + "/build/app/config") \
				  .compile()
		print 'Controller - Done.'

	def parse(self):
		app = App()
		app.setRoot(self.root)\
		   .parse()
		system("cd ../module && make")
		#self.compileView()
		#self.compileController()

	def build(self):
		system("./build.sh")
		
	def proxy(self):
		try:
			server = proxy.Proxy()
			server.setContext(self)
			while True:
				try:
					print  'trying to server ...'
					server.listen()
				except IOError as e:
					print e
					time.sleep(2)
					continue
				break
		except KeyboardInterrupt:
			pass

	def __call__(self, parser, args, values, option_string = None):
		self.root = getcwd();
		if len(values) > 0 :
			self.root += "/" + values
		chdir(self.root)
		self.cwd = self.root

		self.prepare()
		self.parse()
		#self.proxy()

		#Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		#httpd = SocketServer.TCPServer(("", PORT), Handler)
		#print "serving at port", PORT
		#httpd.serve_forever()

		#HttpRequest proxyRequest;
		#HttpResponse proxyResponse;
		#Http server(proxyRequest, proxyResponse);
		
		#server.get("/", [&cwd](Request* _request, Response* _response) {
		#	Debug debug;
		#	debug.setResponse(_response)
		#		 .setViewPath(cwd + "/view")
		#		 .compile();
		#});