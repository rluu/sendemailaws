# Send Email AWS

Author: Ryan Luu  
Email: ryanluu@gmail.com  
GitHub URL: https://github.com/rluu/sendemailaws  
Git Repository URL: https://github.com/rluu/sendemailaws.git  

## Description:

Sends an email using the AWS SES service, from a source email address to a destination email address.  Both these email addresses must be verified within the AWS SES service in order to work.

Also, this software assumes that the AWS credentials and configuration
is set as recommended for use of the AWS SDK.
This means that ~/.aws/credentials and ~/.aws/config contains
the appropriate contents.

## Installation

To install:

```bash
git clone https://github.com/rluu/sendemailaws.git
cd sendemailaws

virtualenv --python=`which python3` venv
source venv/bin/activate

pip install -r conf/pip_requirements.txt
```

## Running

To run the software:

```bash
cd sendemailaws
source venv/bin/activate

python3 src/main.py --from="ryanluu@gmail.com" --to="ryanluu@gmail.com"
```

## Dependencies

- python3

The following python3 dependencies are installed via pip from the pip_requirements.txt file:
- boto3
