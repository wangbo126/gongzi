from flask import Flask
import json
from flask import render_template



app = Flask(__name__)

@app.route('/')
def index():
   #xian shi /home/shiyanlou/files/ zhong json wenjian zhong 'title' liebiao
   title_list = []
   for file_json in "/home/shiyanlou/files/*.json":
       with open(file_json,'r') as f:
           json_dict = json.load(f)
           title_list.append(json_dict['title'])
   print('title_list = {}'.format(title_list))
   return render_template('index.html',title_list)

@app.route('/files/<filename>')
def file(filename):
   #read and  display the content of filename.json 
   #if filename bu cun zai ,then display 'shiyanlou 404' 404 error page
   pass

#http://localhost:3000/ ke jin ru the page of index
if __name__ == '__main__':
    app.run
