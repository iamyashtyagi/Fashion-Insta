import json
import os
from flask import Flask, render_template
from flask import request
from hashtag import get_posts

app = Flask(__name__)

category = dict({'tops': (15047112, 1684544), 'shirt': (14924016, 13278952)})
social_media = set(["Instgram", "Ins", "ins", "Insta"])
social_media_set = set()
print(type(social_media_set))


template ='https://www.myntra.com/'


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


@app.route('/getMetaDataForAStyleImg', methods=['GET'])
def getMetaDataForAStyleImg():
    # In future we would get an image in the requestParam. Currently this is hardcoded.
    # We would call the curl/python client with this image to get the info from style service.
    # image = request.args.get('image')
    # This function scrapes the data from instagram. This will keep running as a batch job.
    # This will kep writing it in the DB and the Cache would get updated.
    get_posts()
    list_of_style = []
    files = os.listdir('/Users/300073043/Desktop/hack/output/')
    for file in files:
        print('file is '+file)
        f = open('/Users/300073043/Desktop/hack/output/'+file)
        data = json.load(f)
        for i in data['response']['styleIds']:
            list_of_style.append(i)
        f.close()
    return render_template('dataloaded.html')


if __name__ == '__main__':
    app.run(debug=True)