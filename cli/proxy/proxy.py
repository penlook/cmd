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

import SimpleHTTPServer
import SocketServer
import urllib2
import os
import time

class ProxyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def response(self):
		if self.path == '/favicon.ico':
			return ""
		if self.path == '/':
			self.server.context.parse()
			self.server.context.build()
			time.sleep(2)
		content = ''
		try:
			content = urllib2.urlopen("http://localhost:8080/").read()
		except Exception as e:
			print e
			content = 'Error !'
		return content

	def do_GET(self):
		self.send_response(200)
		html = self.response()
		self.send_header("Content-length", len(html))
		self.end_headers()
		self.wfile.write(html)
	
	def do_POST(self):
		self.send_response(200)
		html = self.response()
		self.send_header("Content-length", len(html))
		self.end_headers()
		self.wfile.write(html)
	
	def do_HEAD(self):
		self.send_response(200)
		html = self.response()
		self.send_header("Content-length", len(html))
		self.end_headers()
		self.wfile.write(html)
	
	def get_request(self):
		"""Get the request and client address from the socket."""
		# 10 second timeout
		self.socket.settimeout(5.0)
		result = None
		while result is None:
			try:
				result = self.socket.accept()
			except socket.timeout:
				pass
			# Reset timeout on the new socket
			result[0].settimeout(None)
		return result

class Proxy():

	def __init__(self, host = '0.0.0.0', port = 80):
		self.host = host
		self.port = port

	def setContext(self, context):
		self.context = context
	
	def getContext(self):
		return self.context

	def listen(self):
		handler = ProxyHandler
		httpd = SocketServer.TCPServer((self.host, self.port), handler)
		httpd.context = self.getContext()
		print "Serving at port", self.port
		httpd.serve_forever()

