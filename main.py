import urllib.request, urllib.error, urllib.parse, json
from flask import Flask, render_template, request
from secret import API_KEY

app = Flask(__name__)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('form.html',page_title="Booklist Form")

@app.route("/getlist")
def getbooklist():
    list_type = request.args.get('list_type')
    app.logger.info(list_type)

    book_dict = get_book(list=list_type, published_date= 'current')
    booklist = []
    for book in book_dict['results']['books']:
        bookrank = str(book['rank']) + ": " + book['title']
        booklist.append(bookrank)

    return render_template('nytbestselling.html',
                           listname = list_type, bookrank = booklist)

def safeGet(url):
    try:
        return urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e,'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None

def NYTbooks(list = 'hardcover-fiction', published_date = 'current'):
    baseurl = 'https://api.nytimes.com/svc/books/v3/lists'
    api_key = API_KEY
    fullurl = baseurl + "/" + published_date + "/" + list + "?api-key=" + api_key
    return(safeGet(fullurl))

def get_book(list = 'hardcover-fiction', published_date = 'current'):
    book_str = NYTbooks(list=list, published_date=published_date)
    book_data = json.loads(book_str)
    return(book_data)

if __name__ == "__main__":
    app.run(host = "localhost", port = 8080, debug = True)