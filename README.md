django-amazon-catalog
=====================

Create a file ``~/.amazon-product-api`` containing the following data::

    [Credentials]
    access_key = <your access key>
    secret_key = <your secret key>
    associate_tag = <your associate id>



`
 python manage.py fetch_data 11055981 'Beauty'
`

See list of possible sections here (you should use info from column for US) - http://docs.aws.amazon.com/AWSECommerceService/latest/DG/BrowseNodeIDs.html
