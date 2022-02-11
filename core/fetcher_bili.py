import re
from bean.bean import ArticleBean
from core.fetcher_parent import Fetcher as fetcher


def article_bili_url(url):
    """
    通过文章url抓取哔哩哔哩文章

    :param url:文章url
    :return ArticleBean
    :rtype ArticleBean
    """
    content = ''  # 文章内容
    html = fetcher.html_bs_parser(fetcher.http_get(url).text)
    p_list = html.find(id="read-article-holder").find_all('p')  # 文章内容内容放在此标签
    for i in p_list:
        content += i.get_text() + '\n\n'

    title = html.find(property='og:title')['content']

    return ArticleBean(content, title=title)


def article_bili_id(id):
    """
    通过文章ID抓取哔哩哔哩文章

    :param id: 文章ID
    :return: ArticleBean
    :rtype ArticleBean
    """
    return article_bili_url('https://www.bilibili.com/read/cv' + id)


def get_column_ids(column_url):
    """
    获取哔哩哔哩专栏文章的每个文章ID

    :param column_url: 专栏网页url
    :return: 多个ID
    :rtype list
    """
    html = fetcher.http_get(column_url).text
    origin_str = re.search('\\[(.*)]', html).group(1)
    return origin_str.split(',')


def articles_bili_ids(ids):
    """
    抓取哔哩哔哩多个文章

    :param ids: 多个文章ID
    :return: 文章内容
    :rtype str
    """

    content = ""
    for id in ids:
        content += article_bili_id(id).content + "\n\n"
    return ArticleBean(content)


def column(url):
    return ArticleBean(articles_bili_ids(get_column_ids(url)))
