import json
import re

from w3lib import html

from bean.bean import ArticleBean
from core.fetcher_parent import Fetcher as fetcher


def article_baidu_url(url: str):
    """
    只看楼主模式抓取帖子

    :param url: 帖子url
    :return: 文章实体
    :rtype ArticleBean
    """
    id = re.search('p/(\\d+)', url).group(1)
    return article_baidu_id(id)


def article_baidu_id(id: str):
    """
    只看楼主模式抓取帖子

    :param id: 帖子ID
    :return: 文章实体
    :rtype ArticleBean
    """
    result = ''
    url = "https://tieba.baidu.com/p/" + id
    # 拿到帖子页数，+1是为了range循环
    pn = get_pn(id) + 1
    print("page of the post:", pn)

    # 循环抓取每一页
    for p in range(1, pn):
        html_pn = fetcher.html_bs_parser(fetcher.http_get(url + "?see_lz=1&pn=" + str(p)).text)
        print("current url:", url + "?see_lz=1&pn=" + str(p))
        # 所有楼层
        floors = html_pn.find(id='j_p_postlist').find_all(class_='l_post l_post_bright j_l_post clearfix')
        print("number of floors：", len(floors))
        for floor in floors:
            # 拿到json字符串
            data_field = floor['data-field']
            # json字符串转为dict并拿到楼层内容
            content = json.loads(data_field)['content']['content']
            # 去除图片
            content = re.sub("<img(.*)>", '', content)
            # 去除html实体
            content = html.replace_entities(content)
            # 去除<br>换行符
            content = content.replace("<br>", "\n")
            result += content + "\n\n"
    return ArticleBean(result)


def get_pn(id: str):
    """
    获取帖子的pn数，pn是帖子真实的分页数

    :param id: 帖子ID
    :return: pn数
    :rtype int
    """
    html = fetcher.http_get("https://tieba.baidu.com/p/" + id + "?see_lz=1")
    pn = re.search('"pn" : "(.*)", {4}"game_bar_name"', html.text).group(1)
    return int(pn)
