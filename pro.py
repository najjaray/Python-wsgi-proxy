# WSGI proxy
# proxy.py
# file sould be placed in /usr/local/www/wsgi-scripts
# amd mapped to WSGIScriptAlias /proxy

from cgi import parse_qs, escape
import socket, datetime, urllib2

def application(environ, start_response):
	# init response vars
	request_type = '---'
	response_code = '200'
	response_body = 'OK'
	output = None

	# GET url from the GET request
	parameters = parse_qs(environ.get('QUERY_STRING', ''))
	if 'uri' in parameters:
		uri = escape(parameters['uri'][0])
		request_type = environ['REQUEST_METHOD']	
	else:
		uri = 'None'
		response_code = ''
		response_body = ''	
	
	# connet to the remote server
	if uri != None:
		content = urllib2.urlopen(uri)
		if content != None:
			output = content.read()
			response_code = '200'
			response_body = 'OK'	
	status = response_code + ' ' + response_body

	# get the remote server response
	headers = content.info()
	headers['Content-type'] = 'text/html'
	response_headers = [(x, headers[x]) for x in headers]
	start_response(status, response_headers)

	# writing to log file
	with open("/usr/local/www/wsgi-scripts/req.log", "a") as myfile:
		# log syntax 
		myfile.write(datetime.datetime.now().__str__() + "\t" + response_code + "\t" + request_type + "\t" + uri + "\n")
    
	return [output]
