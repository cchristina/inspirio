import random
import sys
from string import punctuation 
import numpy as np
import pandas as pd
import os
import requests
from io import BytesIO
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageDraw2
import textwrap
from datetime import date, timedelta, datetime
from flask import (Flask, render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from colorthief import ColorThief
import pytumblr
from tumblr_keys import client, tumblrblog
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'


quotefile = "./static/json/quotes.json"
quotesdf = pd.read_json(quotefile)

fonts = "./static/fonts/"

cats = ['inspiration',
 'mind',
 'relationship',
 'romance',
 'truth',
 'hope',
 'friendship',
 'purpose',
 'humor',
 'education',
 'quotes',
 'philosophy',
 'funny',
 'god',
 'happiness',
 'science',
 'religion',
 'motivation',
 'wisdom',
 'poetry',
 'soul',
 'writing',
 'love',
 'positive',
 'faith',
 'knowledge',
 'death',
 'books',
 'life',
 'arts',
 'success',
 '',
 '']

def is_real(quote):
    return bool(quotesdf[quotesdf['Quote'].str.contains(quote)].shape[0])


def set_shit_up(category):
    quote_set = set()
    author_set = set()

    for cat in category:
      quote_set.update(set(quotesdf.loc[quotesdf['Category'] == cat.lower()]['Quote']))
      author_set.update(set(quotesdf.loc[quotesdf['Category'] == cat.lower()]['Author']))

    

    quote_words = []
    
    for q in quote_set:
        q = q.strip()
        quote_words.append(q)

    
    split_people = []
    
    author_set = [a.split(',') for a in author_set]

    author_set = [a[0] for a in author_set]

    
    for person in author_set:


        try:
            person = person.split()

            if len(person) == 3:
                split_people.append(person)
            elif len(person) == 2:
                split_people.append([person[0], '', person[1]])
            elif len(person)==1:
                split_people.append([person[0], '', ''])

            else:
                split_people.append([person[0], '', ' '.join(person[2:])])
        except:
            print("fuck ", person)

    return(quote_words, split_people)

def get_mid_factors(num):
    factors = []
    for i in range(1, int(math.sqrt(num))+1):
        if num%i==0:
            factors.append(i)
    return (factors[-1], num//factors[-1])
    
def wrappit(phrase):
    wrapped = textwrap.wrap(phrase)
    wrapped = [words.split() for words in wrapped]
    max_len = max([len(words) for words in wrapped])
    for i, word_list in enumerate(wrapped):
        wrapped[i].extend(['',]*(max_len-len(word_list)))



    wrapped = np.array(wrapped)
    wrapped = wrapped.reshape(get_mid_factors(wrapped.shape[0]*wrapped.shape[1]))


    wrapped = [' '.join([w for w in wrap if w]) for wrap in wrapped]

    return wrapped

def get_fontsize(wrappedtext):
    char_lens = [len(' '.join(w)) for w in wrappedtext]
    char_len = max(char_lens)
    print(char_len)
    return 2000//char_len


def make_chains(quote_words):

    chains = {} 

    quote_words = [q for q in quote_words if len(q.split())>1]
    first_bigs = [(w.split()[0], w.split()[1]) for w in quote_words]
    end_bigs = [(w.split()[-2], w.split()[-1]) for w in quote_words]

    all_words = ' '.join(quote_words) 
    list_of_words = all_words.split()
    
    for i in range(len(list_of_words)-2): 
        bigram = (list_of_words[i], list_of_words[i+1]) 
        if bigram not in chains: 
            chains[bigram]=[] 
        chains[bigram].append(list_of_words[i+2])
        
    return (chains, first_bigs, end_bigs)




def make_thing(chains, first_bigs, end_bigs):

    
    first_bigram=random.choice(first_bigs) 
    words = [] 

    words.append(first_bigram[0]) 
    words.append(first_bigram[1]) 

    next_bigram = first_bigram

    while next_bigram not in end_bigs: 
        try: 
            next_word = random.choice(chains[next_bigram]) 
            words.append(next_word)

            next_bigram=(next_bigram[1], next_word)
            pass
        except KeyError:
            break
    if is_real(' '.join(words)):
        make_thing(chains, first_bigs, end_bigs)
        
    return words



def do_all(category_list):
    words = ""
    q, p = set_shit_up(category_list)
    x,y,z = make_chains(q)

    words = make_thing(x,y,z)
    quotemaster = ' '.join((random.choice(p)[0], random.choice(p)[1], random.choice(p)[2] ))

    print( ' '.join(words), '\n -', quotemaster, "\n\n\n")
    return (words, quotemaster)



def do_all(category_list):
    words = ""
    q, p = set_shit_up(category_list)
    x,y,z = make_chains(q)

    words = make_thing(x,y,z)
    quotemaster = ' '.join((random.choice(p)[0], random.choice(p)[1], random.choice(p)[2] ))

    print( ' '.join(words), '\n -', quotemaster, "\n\n\n")
    return (words, quotemaster)


def make_random_pic(quotespeaker, quotewords):
    
    quotewords = ' '.join(quotewords)
    random_pic = "https://picsum.photos/500"
    response = requests.get(random_pic)
    img = Image.open(BytesIO(response.content))
    img.save( "./static/images/testdel/TEMP.png")

    font_choice = random.choice([f for f in os.listdir(fonts) if not f.startswith(".")])
    font_choice = fonts+font_choice
    print(font_choice, "********* chosen font for words")

    font = TTFont(font_choice)
 



    color_thief = ColorThief("./static/images/testdel/TEMP.png")
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)

    palette = color_thief.get_palette(color_count=3)
    print(palette)

    palette[0] = (palette[0][0], palette[0][1], palette[0][2], 100)

    os.remove("./static/images/testdel/TEMP.png")







    draw = ImageDraw.Draw(img)

    # wrappedtext = wrappit(quotewords)
    wrappedtext = wrappit(quotewords)



    # wrappedtext = textwrap.wrap(quotewords)

    font_size = get_fontsize(wrappedtext)
    print("************", font_size, wrappedtext)

    font = ImageFont.truetype(font_choice, font_size)


    # wrappedtext = textwrap.wrap(quotewords, width=20)

    # if len(wrappedtext) > 10:
    #     font = ImageFont.truetype(font_choice, 40)
    # elif len(wrappedtext) > 12:
    #     font = ImageFont.truetype(font_choice, 30)




    font_choice = random.choice(os.listdir(fonts))
    font_choice = fonts+font_choice

    for i, line in enumerate(wrappedtext):
        print(i, line)
        draw.text((10,(i+1)*font_size),line, fill=palette[0], stroke_width=2, stroke_fill=(palette[0][0]//4, palette[0][1]//4, palette[0][2]//4), font=font)#,  )#,  )
    

    # font_choice = random.choice(os.listdir(fonts))
    # font_choice = fonts+font_choice
    font_choice = random.choice(["./static/fonts/Buda-Light.ttf"])

    print(font_choice, "********* chosen font for person")


    font = ImageFont.truetype(font_choice, 30)
    draw.text((0,50*len(wrappedtext)+font_size*2),quotespeaker, fill=palette[2], stroke_width=1, stroke_fill=(palette[1][0]//4, palette[1][1]//4, palette[1][2]//4), font=font)


    return img


@app.route('/')
def index():
    """Homepage."""


    session["pic"]= session.get('pic', "")
    session["quote"]= session.get('quote', "")
    session["author"]= session.get('author', "")

    # global cats
    cats = ['inspiration',
    'mind',
    'relationship',
    'romance',
    'truth',
    'hope',
    'friendship',
    'purpose',
    'humor',
    'education',
    'quotes',
    'philosophy',
    'funny',
    'god',
    'happiness',
    'science',
    'religion',
    'motivation',
    'wisdom',
    'poetry',
    'soul',
    'writing',
    'love',
    'positive',
    'faith',
    'knowledge',
    'death',
    'books',
    'life',
    'arts',
    'success']

    pic = ""

    return render_template("index.html", cats = cats, pic=session["pic"], q = session["quote"], a= session["author"])


@app.route('/make', methods=['GET', 'POST'])
def make():


    which_cats = []

    for cat in cats:
        include_cat = bool(request.form.get(cat))

        if include_cat:
            which_cats.append(cat)

    if not which_cats:
        which_cats = cats
    final_w, final_q  = do_all(which_cats)

   
    result = make_random_pic(final_q, final_w)
    now = str(datetime.now())
    # savestring = "./static/images/tmpout/INSPIRATION"+now+".png"
    savestring = "./static/images/testdel/INSPIRATION.png"

    result.save(savestring)

    # client = pytumblr.TumblrRestClient(consumer_key, consumer_secret)
    
    session["pic"] = savestring
    session["quote"] = ' '.join(final_w)
    session["author"] = final_q

       
    




    # return render_template("displayimg.html", pic = savestring)
    return redirect("/")

@app.route("/tumblr", methods=['GET'])
def post_to_tumblr():
    # savestring = str(request.args.get("savestring"))
    # client.create_photo(tumblrblog, data=savestring, state="queue")
    flash('sharing to tumblr is currently disabled!')

    return redirect("/")


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug


    # Use the DebugToolbar

    toolbar = DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')