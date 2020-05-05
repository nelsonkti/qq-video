# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import time

class QqvideoPipeline(object):

    def __init__(self):
        # connection database
        self.connect = pymysql.connect('localhost', 'root', '123456', 'n_video')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        print("开始输入数据")
        try:

            if item['title'] is None:
                return

            self.cursor.execute('SELECT * FROM videos WHERE title = "' + item['title'] + '" ')
            data = self.cursor.fetchone()

            print('打印sql')
            print(item['publish_time'])

            if data is None:
                print('【新增视频】数据')
                self.cursor.execute(
                    "insert into videos(title, img_url, publish_time, author, `desc`, sort, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (item['title'], item['img_url'], item['publish_time'], item['author_name'], item['desc'], 0,
                     time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
                self.connect.commit()
            else:
                print('【更新视频】数据')
                self.cursor.execute(
                    "update videos set img_url = %s, publish_time=%s, author=%s, sort=%s,  `desc`=%s, updated_at=%s where id=%s ;",
                    (item['img_url'], item['publish_time'], item['author_name'], 0, item['desc'],
                     time.strftime('%Y-%m-%d %H:%M:%S'), data[0]))
                self.connect.commit()

            print('【查询视频】数据')

            self.cursor.execute('SELECT * FROM videos WHERE title = "' + item['title'] + '" ')
            data = self.cursor.fetchone()

            if data:
                print('查询【视频类型】数据')
                self.cursor.execute('SELECT * FROM category WHERE `name` = %s',
                                    (item['category_name']))
                category = self.cursor.fetchone()
                if category:
                    self.cursor.execute('SELECT * FROM video_to_category WHERE `video_id` = %s and `category_id` = %s',
                                        (data[0], category[0]))
                    video_to_category = self.cursor.fetchone()
                    if video_to_category is None:
                        print('新增【视频和类型关系】数据')
                        self.cursor.execute(
                            "insert into video_to_category(video_id, category_id,created_at, updated_at) values (%s, %s, %s, %s)",
                            (data[0], category[0],
                             time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
                        self.connect.commit()

                video_id = data[0]

                print('查询【视频详情】数据')
                if item['category_name'] == '电影':
                    self.cursor.execute('SELECT * FROM video_series WHERE series_id = %s and video_id = %s',
                                        (1, video_id))
                    data1 = self.cursor.fetchone()

                    print(data1)
                    if data1 is None:
                        print("【新增电影】。。。。")
                        self.cursor.execute(
                            "insert into video_series(video_id, series_id,url,created_at, updated_at) values (%s, %s, %s, %s, %s)",
                            (video_id, 1, item['series'],
                             time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
                        self.connect.commit()
                    else:
                        print("【更新电影】。。。。")
                        self.cursor.execute(
                            "update video_series set url = %s, updated_at=%s where video_id=%s and series_id=%s",
                            (item['series'], time.strftime('%Y-%m-%d %H:%M:%S'), video_id, 1))
                        self.connect.commit()
                # 如果不是电影
                else:
                    for series in item['series']:

                        self.cursor.execute('SELECT * FROM video_series WHERE series_id = %s and video_id = %s',
                                            (series[0], video_id))
                        data1 = self.cursor.fetchone()

                        print(data1)

                        if data1 is None:
                            print("【新增剧集】。。。。")
                            self.cursor.execute(
                                "insert into video_series(video_id, series_id,url,created_at, updated_at) values (%s, %s, %s, %s, %s)",
                                (video_id, series[0], series[1],
                                 time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
                            self.connect.commit()
                        else:
                            print("【更新剧集】。。。。")
                            self.cursor.execute(
                                "update video_series set url = %s, updated_at=%s where video_id=%s and series_id=%s",
                                (series[1], time.strftime('%Y-%m-%d %H:%M:%S'), video_id, series[0]))
                            self.connect.commit()

            print('脚本【完毕】')
        except Exception as error:
            # print error
            print(error)
