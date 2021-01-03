import jieba
import jieba.analyse
import wordcloud


def wordAnalysis(bookname):
    # 生成词云图
    stopWords_dic = open(
        './src/中文停用词表.txt', 'r', encoding='utf-8')     # 从文件中读入停用词
    stopWords_content = stopWords_dic.read()
    stopWords_list = stopWords_content.splitlines()     # 转为list备用
    stopWords_dic.close()

    f = open('./comment/{0}.txt'.format(bookname),
             'r', encoding='utf-8')
    comment = f.read()
    content = jieba.analyse.tfidf(comment, withWeight=False, topK=50)

    txt = ' '.join(jieba.lcut(str(content)))
    f.close()

    w = wordcloud.WordCloud(background_color="black",
                            font_path='./src/粗黑.TTF',
                            width=1600, height=900, scale=1,
                            stopwords=stopWords_list)
    w.generate(txt)
    w.to_file('./picture/{0}.png'.format(bookname))


if __name__ == "__main__":
    wordAnalysis('红楼梦')
