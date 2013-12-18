## in file testing/private/mail_queue.py
import time
query=db(22==db.auth_user.id).select(db.auth_user.email,db.auth_user.first_name)
for q in query:
	inq=db(db.books.id==q.books_issued.book_name).select(db.books.book_name)
	q.book=inq[0].book_name
        context = dict(q=q)
        message = response.render('message.html', context)
        ## Should NOT BE CALLED INDEPENDANTLY    
        db.queue.insert(status='pending', email=q.auth_user.email,subject='Book Overdue',messag=message)
    	db.commit()
rows = db(db.queue.status=='pending').select()
for row in rows:
	if mail.send(to=row.email,subject=row.subject,message=row.messag):
            row.update_record(status='sent')
        else:
            row.update_record(status='failed')
        db.commit()
time.sleep(3*60) # check every minute
    
    
