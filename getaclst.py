#! /usr/bin/env python2.7

# genaclst.py
#
# Generate accounts document in ADF 3. format
# Run this in the Master account to create documentation for existing accounts
# Assumes ROLE in child accounts to find account alias
#
# (c) erik@easytocloud.com
#

from __future__ import print_function

import boto3
from botocore.exceptions import ClientError

ROLE='OrganizationAccountAccessRole'
CREATED_ONLY=True

org = boto3.client('organizations')

# recursive function to walk the tree up from account via parent OUs to ROOT

def get_ou_path(Id):
    
    ouPath = ''
    
    parent = org.list_parents(ChildId = Id)['Parents'][0]
    
    if parent['Type'] == 'ORGANIZATIONAL_UNIT':
        ou = org.describe_organizational_unit(OrganizationalUnitId = parent['Id'])['OrganizationalUnit']
   
        ouPath = get_ou_path(ou['Id'])+'/'+ou['Name']
    
    return ouPath

def get_account_alias(a):
    # this requires a role to be assumed in the very account you want to find the alias for
    
    iam_client = boto3.client('iam')
    sts_client = boto3.client('sts')

    alias=str(a['Name'])

    if a['Id'] != sts_client.get_caller_identity()['Account']:
        
      try:
        assumedRoleObject = sts_client.assume_role(
          RoleArn="arn:aws:iam::"+str(a['Id'])+":role/"+ROLE,
          RoleSessionName="AliasGetter"
        )

        credentials = assumedRoleObject['Credentials']

        iam_client = boto3.client(
          'iam',
          aws_access_key_id = credentials['AccessKeyId'],
          aws_secret_access_key = credentials['SecretAccessKey'],
          aws_session_token = credentials['SessionToken'],
        )
        aliases = iam_client.list_account_aliases()
        if len(aliases['AccountAliases']) > 0:
            alias=aliases['AccountAliases'][0]
            
      except:
        pass
    else:
        iam_client = boto3.client('iam')
        aliases = iam_client.list_account_aliases()
        
        if len(aliases['AccountAliases']) > 0:
            alias=aliases['AccountAliases'][0]
            
    print('    alias:',alias.replace("_","-").replace(" ", "-").lower())
    
    
def acct_out(a):

    if CREATED_ONLY == True & (str(a['JoinedMethod']) != 'CREATED') :
      return

    print('  # accountId', str(a['Id']) )
    print('  # ', str(a['JoinedMethod']))
    
    print('  - account_full_name: "'+ str(a['Name'])+ '"')
    print('    organizational_unit_path: ', get_ou_path(a['Id']))
    print('    email: ', str(a['Email']))
    print('    allow_billing: True')
    print('    delete_default_vpc: False')
    
    get_account_alias(a)
    
    print('    tags:')
    print('      - created_by_adf: False')
    print('')

'''

Example of the .yml file according to the documentation

accounts:
  - account_full_name: company-test-1
    organizational_unit_path: /business-unit1/test
    email: test-team-1@company.com
    allow_billing: True
    delete_default_vpc: False
    alias: test-company-11
    tags:
      - created_by: adf
      - environment: test
      - costcenter: 123
'''
  

def main():
    
    print('accounts:')
   
    accounts = org.list_accounts()
    
    while True:
        for account in accounts['Accounts']:
            acct_out(account)
        
        if 'NextToken' in accounts:
            accounts = org.list_accounts(NextToken = accounts['NextToken'])
        else:
            break

main()

{
            "Status": "ACTIVE", 
            "Name": "cb-redac-prod", 
            "Email": "aws+redacprod@cb.nl", 
            "JoinedMethod": "CREATED", 
            "JoinedTimestamp": 1530863535.481, 
            "Id": "380837003961", 
            "Arn": "arn:aws:organizations::489407789817:account/o-qizqp7x923/380837003961"
        }, 

