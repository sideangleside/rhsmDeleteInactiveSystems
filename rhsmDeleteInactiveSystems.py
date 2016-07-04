#!/usr/bin/env python

# File: rhsmShowConsumerSubs.py
# Author: Rich Jerrido <rjerrido@outsidaz.org>
# Purpose: Given a username & password, query
# 		   Red Hat Subscription Management (RHSM) to show a
# 		   listing of consumers and their associated subscriptions
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import getpass
import urllib2
import base64
import sys
import ssl
import time
from datetime import date
from optparse import OptionParser

today = date.today()
parser = OptionParser()
parser.add_option("-l", "--login", dest="login", help="Login user for RHSM", metavar="LOGIN")
parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted", metavar="PASSWORD")
parser.add_option("-d", "--debug", dest='debug',help="print more details for debugging" , default=False, action='store_true')
parser.add_option("--delete", dest='delete',help="Actually delete systems (will only report on inactive systems if omitted)" , default=False, action='store_true')
parser.add_option("--days", dest="daysback", type=int, help="Number of days of inactivity to consider systems for deletion", metavar="DAYSBACK")
(options, args) = parser.parse_args()

if not ( options.login and options.daysback ):
	print "Must specify a login and # of days of inactivity (will prompt for password if omitted).  See usage:"
	parser.print_help()
	print "\nExample usage: ./rhsmDeleteInactiveSystems.py -l rh_user_account --days 30"
	sys.exit(1)
else:
	login = options.login
	password = options.password
	daysback = options.daysback


if not password: password = getpass.getpass("%s's password:" % login)

if hasattr(ssl, '_create_unverified_context'):
	        ssl._create_default_https_context = ssl._create_unverified_context

portal_host = "subscription.rhn.redhat.com"
class error_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

#### Grab the Candlepin account number
url = "https://" + portal_host + "/subscription/users/" + login + "/owners/"
try:
 	request = urllib2.Request(url)
        if options.debug :
            print "Attempting to connect: " + url
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

accountdata = json.load(result)
for accounts in accountdata:
	acct = accounts["key"]

#### Grab a list of Consumers
url = "https://" + portal_host + "/subscription/owners/" + acct + "/consumers/"
if options.debug :
     print "Attempting to connect: " + url

try:
 	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (login, password)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Error: cannot connect to the API: %s" % (e)
	print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
	sys.exit(1)
except:
	print "FATAL Error - %s" % (e)
	sys.exit(2)

consumerdata = json.load(result)

#### Now that we have a list of Consumers, loop through them and 
#### List the subscriptions associated with them. 
for consumer in consumerdata:
	consumerType = consumer["type"]["label"]
	lastCheckin = consumer["lastCheckin"]
	username = consumer["username"]
	# Only delete consumers of type 'system'. Ignores type hypervisor or Satellite
        if consumerType == "system":
            # Some systems report 'None' as their lastCheckIn value. Skip these as
            # we dont have enough data to determine if they should be deleted. 
            if lastCheckin == None:
                print "=" * 80
                print "\t Skipping host - %s as it doesn't have a valid lastCheckin value" % consumer["name"]
                continue
            rhsmdate=str(lastCheckin)
            working_rhsm_date=date(int(rhsmdate[0:4]), int(rhsmdate[5:7]), int(rhsmdate[8:10]))
            days_ago = abs(today - working_rhsm_date)
            if days_ago.days > daysback:
                print "=" * 80
                print "\t Consumer Name - %s" % consumer["name"]
                print "\t Consumer UUID - %s" % consumer["uuid"]
                print "\t Last Check-in - %s" % lastCheckin
                print "\t Registered User - %s" % username
                print "\t %s will be deleted as it as has not checked in within %s" % (consumer["name"],days_ago)
                if options.delete:
                    print "\t Attemping delete of %s%s%s" % (error_colors.WARNING,consumer["name"],error_colors.ENDC)
                    url = "https://" + portal_host + "/subscription/consumers/" + consumer["uuid"] + "/"
                    try:
                        request = urllib2.Request(url)
                        base64string = base64.encodestring('%s:%s' % (login, password)).strip()
                        request.add_header("Authorization", "Basic %s" % base64string)
                        request.get_method = lambda: "DELETE"
                        result = urllib2.urlopen(request)
                        # if Candlepin Returns HTTP 204 - 'No Content', it has successfully deleted the system
                        # otherwise it did not
                        httpStatusCode = result.getcode()
                        if httpStatusCode == 204:
                            print "\t Result - %sSUCCESS%s" % (error_colors.OKBLUE,error_colors.ENDC)
                        else:
                            print "\t Result - %sFAILURE%s - Server Reports HTTP %s" % (error_colors.FAIL,error_colors.ENDC,httpStatusCode)
                    except urllib2.URLError, e:
                        print "Error: cannot connect to the API: %s" % (e.reason)
                        print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
                        sys.exit(1)
                    except urllib2.HTTPError, e:
                        print "Error: HTTP Error %s" % (e.code)
            else:
                print "=" * 80
                print "\t Skipping host - %s as it doesn't meet the deletion criteria" % consumer["name"]
