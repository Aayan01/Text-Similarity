from xml.dom.minidom import Document
import en_core_web_lg
from flask import request
from flask import Flask, render_template

# defining the webpage
app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    # defining the spacy model
    nlp = en_core_web_lg.load()
    #print("small model: ", nlp)
    sentence1 = request.form['text1']
    sentence2 = request.form['text2']
    # sentence1 = "i'm a scared boy"
    # sentence2 = "i'm a terrified cat"
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    output = str(round(doc1.similarity(doc2), 2)*100) + '%'
    print("Similarity between 2 doc", output)
    return(render_template('index.html', variable=output))


if __name__ == "__main__":
    app.run(port='5500', threaded=False)
