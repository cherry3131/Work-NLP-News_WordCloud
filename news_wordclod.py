# python WordCloud(BBC NEWS)

from lxml import etree
import requests
import jieba
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud

def scrape_articles(url, headers, pages, sleep_time=2):
    article_title_list = []
    page = 1
    
    for _ in range(pages):
        try:
            res = requests.get(url % page, headers=headers, timeout=30)
            res.raise_for_status()  
            soup = BeautifulSoup(res.text, "html.parser")
            title_tags = soup.find_all('h2', class_='bbc-10m3zrw e47bds20')

            for title in title_tags:
                title_list = title.text
                article_title_list.append(title_list)
            
            page += 1
            time.sleep(sleep_time)
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            break  # Exit loop if there's an error
    
    all_articles = '\n'.join(article_title_list)
    return all_articles

def key_words(all_articles):
    seg_stop_words_list = []
    seg_words_list = jieba.lcut(all_articles)

    with open(file='./jieba_data/stop_words.txt', mode='r', encoding='utf-8') as file:
        stop_words = file.read().split('\n')

    # key words(result after stop words are removed)
    seg_words_list = jieba.lcut(all_articles)
    for word in seg_words_list:
        if word not in stop_words:
            seg_stop_words_list.append(word)    
    return(seg_stop_words_list)

def create_wordcloud(seg_stop_words_list, pic_path='./Tree.png'):
    seg_words = ' '.join(seg_stop_words_list)
    pic = np.array(Image.open(pic_path))
    my_wordcloud = WordCloud(font_path='msjh.ttc', background_color="white", mask=pic, contour_width=3, contour_color='steelblue').generate(seg_words)
    my_wordcloud.to_file('wordcloud.jpg') #output the picture
    
    # wordcloud
    plt.imshow(my_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    print("create!")


# # Main program
url = "https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt?page=%s"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0"
}
pages = 5  #  scrape 5 pages
all_articles = scrape_articles(url, headers, pages)
print(all_articles,'success!')


seg_stop_words_list = key_words(all_articles)

create_wordcloud(seg_stop_words_list)
