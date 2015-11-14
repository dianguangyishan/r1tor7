from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from models import Book, Author
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def home(request):
	author=request.REQUEST.get("author","")
	if author!="":
		tmp=Author.objects.filter(Name=author)
		j=0
		for i in tmp:
			j=j+1
		if j!=0:
			booklist=Book.objects.filter(AuthorID = tmp)
		else:
			booklist = Book.objects.all()
	else:
		booklist = Book.objects.all()
	return render_to_response('home.html',Context({"booklist":booklist,}))
@csrf_exempt
def delete(request):
	book = Book.objects.filter(id = request.GET["id"])
	book.delete()
	return render_to_response('jump.html')
@csrf_exempt
def add(request):
	if request.POST:
		post=request.POST
		author = Author.objects.get(Name = post["author"])
		new_book=Book(
		ISBN = post["isbn"],
		Title = post["title"],
		AuthorID = author,
		Publisher = post["publisher"],
		PublishDate = post["publishdate"],
		Price = post["price"])
		new_book.save()
		return render_to_response('jump.html')
	else:
		authorlist = Author.objects.all()
		return render_to_response('new.html',Context({"authorlist":authorlist,}))
@csrf_exempt
def modify(request):
	book = Book.objects.get(id = request.GET["id"])
	authorlist = Author.objects.all()
	if request.POST:
		post=request.POST
		author = Author.objects.get(Name = post["author"])
		book.ISBN = post["isbn"]
		book.Title = post["title"]
		book.AuthorID = author
		book.Publisher = post["publisher"]
		book.PublishDate = post["publishdate"]
		book.Price = post["price"]
		book.save()
		booklist = Book.objects.all()
		return render_to_response('jump.html')
	return render_to_response('modify.html',Context({"book":book,"authorlist":authorlist,}))
def info(request):
	booklist = Book.objects.filter(id = request.GET["id"])
	for book in booklist:
		author = book.AuthorID
	return render_to_response('crud.html',Context({"booklist":booklist,"author":author,}))
@csrf_exempt
def addauthor(request):
	if request.POST:
		post = request.POST
		new_author = Author(
		 AuthorID = post["authorID"],
		 Name = post["name"],
		 Age = post["age"],
		 Country = post["country"]
		)
		new_author.save()
		return HttpResponseRedirect("/add/")
	return render_to_response('addauthor.html')