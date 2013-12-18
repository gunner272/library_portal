# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
from plugin_rating_widget import RatingWidget


################################ The core ######################################
# Inject the horizontal radio widget

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate,Mail,datetime
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

#from gluon.tools import Recaptcha
#auth.settings.captcha = Recaptcha(request,
#    '6Ldt0t4SAAAAANR-uOP_LPZiUAsRk9CVK1AcWwFr', '6Ldt0t4SAAAAAMigT-0uRVyuiZIKCXLBIY_YGYdi')


db.define_table('books',
		db.Field('book_name','string',required=True),
		db.Field('author','string',required=True),
		db.Field('publication_house','string',required=True),
		db.Field('category','string',requires=IS_IN_SET(["general knowledge","religion","economics","maths","physics","english","other languages","programming languages","computer science"])),
		db.Field('sub_category','string',requires=IS_IN_SET(["sports","current affairs","entertainment","technology","hindu","christian","buddhism","muslim","parsi","sikh","macro","micro","statistics","algebra","number theory","calculus","geometry","fluid dynamics","optics","thermodynamics","electromagnetism","quantum computing","poetry","drama","hindi","telegu","c++","java","python","perl","php","html","xml","computer system organization","network","security"])),  # sub_category based on category, a drop down box will appear
		db.Field('book_location',"integer",writable='False'),   #location based on sub_category,a drop down box will appear
		db.Field('availability','integer',requires=IS_IN_SET([0,1]),default=1,readable=False,writable=False),
		db.Field('reference','string',requires=IS_IN_SET(["Reference Copy","Issueable Book"]),widget=SQLFORM.widgets.radio.widget),
		db.Field('noofrating','integer',readable=False,writable=False,default=1),
		db.Field('rating', 'integer',requires=IS_IN_SET(range(1, 6)),widget=RatingWidget(),default=1),
		db.Field('am','integer',readable=False,writable=False,default=1),
		db.Field('summary','text'))

auth.settings.extra_fields['auth_user']=[
Field('rollno','integer',required=True,requires=IS_NOT_IN_DB(db,'auth_user.rollno')),
Field('gender','string',requires=IS_IN_SET(['Male','Female']),default='Male',widget=SQLFORM.widgets.radio.widget),
Field('security_ques','string',required=True),
Field('security_ans','string',requires=CRYPT(),readable=False,required=True),
Field('preference_1','string',db.books,requires=IS_IN_SET(["general knowledge","religion","economics","maths","physics","english","other languages","programming languages","computer science"])),
Field('preference_2','string',db.books,requires=IS_IN_SET(["general knowledge","religion","economics","maths","physics","english","other languages","programming languages","computer science"])),
Field('preference_3','string',db.books,requires=IS_IN_SET(["general knowledge","religion","economics","maths","physics","english","other languages","programming languages","computer science"])),
Field('preference_4','string',db.books,requires=IS_IN_SET(["general knowledge","religion","economics","maths","physics","english","other languages","programming languages","computer science"])),
Field('preference_5','string',db.books,requires=IS_IN_SET(["general knowledge","religion","economics","maths","physics","english","other languages","programming languages","computer science"]))]

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail=Mail()  # uncomment this to enable sending email programmatically
mail.settings.server='students.iiit.ac.in:25'   # your SMTP server
mail.settings.sender='rishabh.sharma@students.iiit.ac.in'  # your email

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
#db.define_table('category',db.Field('name'))
#db.define_table('color', db.Field('category', db.category), Field('name'))
#db.define_table('product',
#    db.Field('category', db.category, comment='<- type "A" or "B"'),
#    db.Field('color', db.color,
#          requires=IS_EMPTY_OR(IS_IN_DB(db(db.color.id > 0), 'color.id', 'color.name', zero='---')),
 #         comment='<- select category first'),
  #  )
         #time should automatically be updated
#db.define_table('users',
#		db.Field('name','string',required=True),
#		db.Field('rollno','integer',unique=True,required=True),
#		db.Field('gender','string',IS_IN_SET(['male','female'])),
#		db.Field('email','string',requires=IS_EMAIL()),
#		db.Field('password','password',required=True,comment="make it strong"),
#		db.Field('security_ques','string',required=True),
#		db.Field('security_ans','string',required=True),
		#db.Field('preference_1','string',db.books,requires=IS_IN_DB(db,db.books.category,db.books.category)),
		#db.Field('preference_2','string',db.books,requires=IS_IN_DB(db,db.books.category,db.books.category)),
		#db.Field('preference_3','string',db.books,requires=IS_IN_DB(db,db.books.category,db.books.category)),
		#db.Field('preference_4','string',db.books,requires=IS_IN_DB(db,db.books.category,db.books.category)),
		#db.Field('preference_5','string',db.books,requires=IS_IN_DB(db,db.books.category,db.books.category)))
db.define_table('books_issued',
		db.Field('user_rollno',db.auth_user,required=IS_IN_DB(db,"auth_user.id","auth_user.rollno")), #testing if it works without the 3rd argument
		db.Field('book_name',db.books,required=IS_IN_DB(db,db.books.id,db.books.book_name)), # testing the same in this
		db.Field('date_of_issue','datetime',required=True,default=request.now),
		db.Field('date_of_return','datetime',required=True,default=request.now+datetime.timedelta(days=14)),
		db.Field('date_of_comeback','datetime'))
db.define_table('block_issue',
		db.Field('user_rollno',db.auth_user,required=IS_IN_DB(db,db.auth_user.id,db.auth_user.rollno)),
		db.Field('book_name',db.books,requires=IS_IN_DB(db,db.books.id,db.books.book_name),required=True))
db.define_table('book_comment',
		db.Field('book_name',db.books,required=IS_IN_DB(db,db.books.id),readable=False,writable=False),
		db.Field('commenting_user',db.auth_user,required=IS_IN_DB(db,db.auth_user.id),readable=False,writable=False),
		db.Field('comment_on_book','string'),
		db.Field('comment_time','datetime',default=request.now,writable=False,readable=False))    #time should automatically be updated
db.define_table('request_book',
		db.Field('book_name','string',required=True),
		db.Field('author','string',required=True),
		db.Field('publication_house','string',required=True))

db.define_table('queue',Field('status','string'),Field('email',requires=IS_EMAIL()),Field('subject','string'),Field('messag','text'))


db.define_table('post', Field('your_message', 'text'))
db.post.your_message.requires = IS_NOT_EMPTY()

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
