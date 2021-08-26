import json
import os
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

category = dict({'shoes': (15047112, 1684544), 'shirt': (14924016, 13278952)})
social_media = set(["Instgram", "Ins", "ins", "Insta"])
social_media_set = set()
print(type(social_media_set))


template ='https://www.myntra.com/'

def curl(fileName):
    os.system("sh curl.sh "+fileName)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html' )

@app.route('/getTrendingByCategory', methods=['GET'])
def getTrendingByCategory():
    query = request.args.get('query')
    queries = query.split()
    cat = queries[1]
    website = queries[0]
    if len(queries) > 2 or website not in social_media or cat not in category.keys():
        return "You should type the query in this format -> SocialMedia Category -> Instagram Shoes"
    return render_template('shoetrending.html')


@app.route('/getMetaDataForAStyleImg', methods=['POST'])
def getMetaDataForAStyleImg():
    # In future we would get an image in the requestParam. Currently this is hardcoded.
    # We would call the curl/python client with this image to get the info from style service.
    image = request.args.get('image')
    # This function scrapes the data from instagram. This will keep running as a batch job.
    # This will kep writing it in the DB and the Cache would get updated.
    # get_posts()
    curl()
    f = open('/Users/300071202/IdeaProjects/Fashion-Insta/out2.json')
    data = json.load(f)
    list_of_style = []
    for i in data['response']['styleIds']:
        list_of_style.append(i)
    f.close()


if __name__ == '__main__':
    app.run(debug=True)