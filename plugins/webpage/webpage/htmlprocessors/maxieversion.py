# -*- coding: UTF-8 -*-


def maxIEVersion (params):
    meta_tag = params.soup.new_tag ('meta')
    meta_tag['http-equiv'] = 'x-ua-compatible'
    meta_tag['content'] = 'IE=edge'
    params.soup.head.insert(0, meta_tag)
