from flask import Flask,render_template,request,jsonify
import requests
import database
from spell_check1 import find_invalid_word
from logging.handlers import RotatingFileHandler

#flask object
app=Flask(__name__,
template_folder="clients/templates",
static_folder="clients/static")

file_handler = RotatingFileHandler("error.log", maxBytes=1024 * 1024 * 100)
app.logger.addHandler(file_handler)

@app.errorhandler(500)
def handle_500_error(exception):
    app.logger.error(exception)
    return "Internal Server Error"

@app.errorhandler(404)
def handle_404_error(exception):
    app.logger.error(exception)
    return "Not Found"

#function to get html page
@app.route("/")
def get_html():
    print("html page")
    return render_template("spell_check.html")


#function to get invalid words
@app.route("/api/get_invalid_words",methods =['GET'])
def spell_checker():
    content = request.args.get("content")
    print("getting content from webpage")
    invalid_words = find_invalid_word(content)
    if type(invalid_words)==str:
        return jsonify(invalid_words)
    else:
        word_list=list()
        for key in invalid_words:
            
            output=str()
            output="\nline:"+str(key)+"\nwords:"+str(invalid_words[key])+"\n"
            word_list.append(output)
        return jsonify(word_list)

if __name__ == '__main__':
    app.run(port=3000)