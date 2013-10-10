# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt 
from __future__ import unicode_literals
import webnotes
from webnotes.utils import cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def autoname(self):
		self.doc.name = self.doc.dt + "-" + self.doc.script_type

	def validate(self):
		if self.doc.script_type=="Server" and webnotes.session.user!="Administrator":
			webnotes.throw("Only Administrator is allowed to edit Server Script")

		# fix indentation
		tabs = None
		for line in self.doc.script.split("\n"):
			if line.strip():
				for i, char in enumerate(line):
					if char=="\t":
						tabs = "\t"
						break
					if char!=" ":
						if i==0:
							webnotes.throw("Custom Script must be indented by one tab")
						tabs = " " * i
						break
			if tabs: 
				break
		
		self.doc.script = self.doc.script.replace(tabs, "  ")
		if not self.doc.script.startswith("\n"):
			self.doc.script = "\n" + self.doc.script

	def on_update(self):
		webnotes.clear_cache(doctype=self.doc.dt)
		webnotes.cache().delete_value("_server_script:" + self.doc.dt)
	
	def on_trash(self):
		webnotes.clear_cache(doctype=self.doc.dt)
		webnotes.cache().delete_value("_server_script:" + self.doc.dt)

def get_custom_server_script(doctype):
	custom_script = webnotes.cache().get_value("_server_script:" + doctype)
	if not custom_script:
		custom_script = webnotes.conn.get_value("Custom Script", {"dt": doctype, "script_type":"Server"}, 
			"script") or ""
		webnotes.cache().set_value("_server_script:" + doctype, custom_script)
	
	return custom_script

