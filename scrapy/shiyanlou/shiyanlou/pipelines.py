# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, User, engine
from scrapy.exceptions import DropItem
from datetime import datetime
from shiyanlou.items import CourseItem, UserItem

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        """
        # 提取的学习人数是字符串,把它转换成 int
        item['students'] = int(item['students'])
        if item['students'] < 1000:
            # 对于不需要的 item, 主动触发 DropItem 异常
            raise DropItem('Course students less than 1000.')
        else:
        # 根据 item 创建 Course Model 对象并添加到 session
        # item 可以当成字典来用, 所以也可以使用字典解构, 相当于
        # Course(
        #    name=item['name'],
        #    type=item['type'],
        #    ...,
        # )
            self.session.add(Course(**item))
        return item

        """
        # 对不同的 item 使用不同的处理函数
        if isinstance(item, CourseItem):
            self._process_course_item(item)
        else:
            self._process_user_item(item)
        return item

    def _process_course_item(self, item):
        item['students'] = int(item['students'])
        self.session.add(Course(**item))

    def _process_user_item(self, item):
        # 抓取到的数据类似 'L100', 需要去掉 'L' 然后转化为 int
        item['level'] = int(item['level'][1:])
        # 抓取到的数据类似 '2017-01-01 加入实验楼', 把其中的日期字符串转换为date对象
        item['join_date'] = datetime.strptime(item['join_date'].split()[0], '%Y-%m-%d')
        # 学习课程数目转化为 int
        item['learn_courses_num'] = int(item['learn_courses_num'])
        # 添加到 session
        self.session.add(User(**item))
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
        
