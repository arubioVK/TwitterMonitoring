#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

patronidiomaactive = "(es|en|fr|de|it)$"
patronubicacionactive ="(US|ES|PT|FR|GB|DE|IT)$"
patronhora="(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$"
patronurl="(.*ovemago\.com.*|.*platzi\.es.*|.*paypal\.com.*)$"
patronpalabrotas="(.*palurdo.*|.*caraculo.*|.*capullo.*|.*lerdo.*|.*polla.*|.*cipote.*|.*tocapelotas.*|.*gilipollas.*|.*subnormal.*|.*puta.*|.*hdp.*|.*malparido.*|.*mierdaseca.*|.*cabron.*|.*lameculos.*|.*tolai.*)$"

def expidiomaactive(idioma):
	return re.match(patronidiomaactive, idioma) is not None
def expubicacionactive(ubicacion):
	return re.match(patronubicacionactive, ubicacion) is not None
def exppatronhora(hora):
	return re.match(patronhora,hora) is not None
def exppatronurls(url):
	return re.match(patronurl, url.lower()) is not None
def exppatronpalabrotas(frase):
	return re.match(patronpalabrotas, frase.lower()) is not None


