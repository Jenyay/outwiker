# -*- coding: UTF-8 -*-


def maxIEVersion(params):
    meta_tag = params.soup.new_tag('meta')
    meta_tag['http-equiv'] = 'x-ua-compatible'
    meta_tag['content'] = 'IE=edge'
    if params.soup.head is None:
        head = params.soup.new_tag('head')
        params.soup.insert(0, head)
    params.soup.head.insert(0, meta_tag)
