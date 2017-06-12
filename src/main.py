#!/usr/bin/env python3
##############################################################################
# Description:
#   Sends a sample email to a destination email address using AWS SES
#   email service.
#
# Usage:
#
#     python3 main.py --help
#     python3 main.py --version
#     python3 main.py --from="ryanluu@gmail.com" --to="ryanluu@gmail.com"
#
# Note:
#     This application assumes that the AWS credentials and configuration
#     is set as recommended for use of the AWS SDK.
#     This means that ~/.aws/credentials and ~/.aws/config contains
#     the appropriate contents.
#
# 
##############################################################################

import sys
import os
import datetime
import logging
import logging.handlers
import logging.config

import boto3

# For parsing command-line options
from optparse import OptionParser

##############################################################################
# Global variables
##############################################################################

__version__ = "1.0.0"
__date__ = "Mon Jun 12 00:26:35 EDT 2017"


# Application Name
APP_NAME = "Send Email AWS"

# Application Version obtained from subversion revision.
APP_VERSION = __version__

# Application Date obtain from last subversion commit date.
APP_DATE = __date__

# Location of the source directory, based on this script file.
SRC_DIR = os.path.abspath(sys.path[0])

# Directory where log files will be written.
LOG_DIR = \
    os.path.abspath(os.path.join(SRC_DIR,
                                 ".." + os.sep + "logs"))

# Location of the config file for logging.
LOG_CONFIG_FILE = \
    os.path.abspath(os.path.join(SRC_DIR,
                                 ".." + os.sep +
                                 "conf" + os.sep +
                                 "logging.conf"))

# For logging.
logging.config.fileConfig(LOG_CONFIG_FILE)
log = logging.getLogger("main")


# These globals are extracted from command-line arguments.
fromEmailAddress = None
toEmailAddress = None

# Email contents' values.
emailSubject = "Test email from the '" + APP_NAME + "' application."
endl = "\n"
emailBodyText = "Hi, " + endl + \
    endl + \
    "  This Text email was sent via AWS SES.  " + \
    "I hope you have a nice day!" + endl + \
    endl + \
    "-Ryan & Ryan"
endl = "<br />"
emailBodyHtml = "Hi, " + endl + \
    endl + \
    "  This HTML email was sent via AWS SES.  " + \
    "I hope you have a nice day!" + endl + \
    endl + \
    "-Ryan &amp; Ryan"



##############################################################################
# Methods
##############################################################################

def shutdown(rc):
    """
    Exits the script, but first flushes all logging handles, etc.
    """
    
    logging.shutdown()
    sys.exit(rc)


def sendEmail():
    log.debug("Sending email from " + fromEmailAddress + " to " + \
              toEmailAddress + " ...")

    client = boto3.client('ses')
    response = client.send_email(
        Destination={
            'ToAddresses': [toEmailAddress],
            'CcAddresses': [],
            'BccAddresses': []
            },
        Message={
            'Subject': {
                'Data': emailSubject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': emailBodyText,
                    'Charset': 'UTF-8'
                    },
                'Html': {
                    'Data': emailBodyHtml,
                    'Charset': 'string'
                    }
                }
            },
        ReplyToAddresses=[],
        ReturnPath='',
        ReturnPathArn='',
        SourceArn='',
        Source=fromEmailAddress,
        )
    
    log.debug("Sending email done.")
    log.debug("Response is: " + str(response))

##############################################################################
# Main
##############################################################################

if __name__ == "__main__":
    log.info("##########################################################")
    log.info("# Starting " + APP_NAME + \
             " (" + sys.argv[0] + "), version " + APP_VERSION)
    log.info("##########################################################")

    # Create the parser
    parser = OptionParser()

    # Specify all valid options.
    parser.add_option("-v", "--version",
                          action="store_true",
                          dest="version",
                          default=False,
                          help="Display script version info and author contact.")

    parser.add_option("--from",
                          action="store",
                          type="str",
                          dest="fromEmailAddress",
                          default=None,
                          help="Specify the sender's email address.  " + \
                          "This email address must be a verified email address in AWS SES.  " + \
                          "This is a required field.",
                          metavar="<EMAIL_ADDRESS>")

    parser.add_option("--to",
                          action="store",
                          type="str",
                          dest="toEmailAddress",
                          default=None,
                          help="Specify the destination email address.  " + \
                          "This email address must be a verified email address in AWS SES.  " + \
                          "This is a required field.",
                          metavar="<EMAIL_ADDRESS>")


    # Parse the arguments into options.
    (options, args) = parser.parse_args()

    # Print version information if the flag was used.
    if options.version == True:
        print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
        print("By Ryan Luu, ryanluu@gmail.com")
        shutdown(0)

    if options.fromEmailAddress == None:
        log.error("Please specify an email address to the " + \
                 "--from option.")
        shutdown(1)
    else:
        fromEmailAddress = options.fromEmailAddress.strip()
       
    if options.toEmailAddress == None:
        log.error("Please specify an email address to the " + \
                  "--to option.")
        shutdown(1)
    else:
        toEmailAddress = options.toEmailAddress.strip()

    sendEmail()
        
    log.info("Done.")
    shutdown(0)

##############################################################################
