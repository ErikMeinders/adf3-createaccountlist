# adf3-createaccountlist

Create list of your existing AWS accounts in ADF 3 account.yml format.

Tool to create an account.yml list for all your current account.

Run this in your Organization Master account in your checked-out aws-deployment-framework-bootstrap repo.

`
adf3-createaccountlist > adf-accounts/preADF3existingaccounts.yml
`

# options

In the source code you can change some 'constants'

`ROLE=OrganizationAccountAccessRole
`

Change this to the name of the role the tool should assume in your child accounts.

`CREATED_ONLY=True
`

You can indicate that you want only the CREATED (as opposed to INVITED) accounts.
Created account will have an OrganizationAccountAccessRole (or whatever name your organization uses).
Invited accounts might lack that Role as they were created outside of your organization and thus no have a standard Role name.
Therefor this tool might not be able to assume it.

# WARNING

Check the output before you commit it to master. If everything is correct, ADF will recognize the accounts in the file 
as existing accounts and not make any changes.
