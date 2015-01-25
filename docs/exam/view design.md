
# View Design of Exam
本文档包含两个部分，分别是ViewFuncs和Views

+ ViewFuncs 在Views中需要使用的辅助方法
+ Views 视图模块

## ViewFuncs

### 数据拉取相关
这一部分的方法用于从数据库中拉取少量数据并进行重组织，然后保存到缓存中

用到的常量 cc.OPTIONAL_ANS, cc.QUESTIONS, cc.TAGS, cc.CATEGORIES

测试点：是否得到正确数据，是否放入cache

#### getCachedOptionalAnswers()
拉取OptionalAnswer数据保存于cache[cc.OPTIONAL_ANS]中，格式为dict，注意其key直接为OptionalAnswer的ID值，dict具体为

```python
{
    id: {
        'content': 'str',
        'qid': question_id,
        'is_sln': boolean,
    },
}
```

#### getCachedQuestions()
拉取Question数据，保存于cache[cc.QUESTIONS]中

```python
{
    id: {
        'content': 'str',
        'tid': tag_id,
        'level': num,
        'op_ans': [op_ans_ids,],
    },
}
```

### getCachedTags()
拉取Tag数据，保存于cache[cc.TAGS]中

```python
{
    id: {
        'name': 'str',
        'cid': category_id,
        'questions': [question_ids,],
        'question_dist': [{
          'level': num,
          'count': count,
        }],
    },
}
```

### getCachedCategory()
拉取Category数据，保存于cache[cc.CATEGORIES]中，注意这次的key为Category的name

```python
{
    'name': {
        'id': category_id,
        'n_min': num,
        'n_max': num,
        'v_step': num,
        'v_base': num,
        'free_time': num,
        'max_time': num,
        'tags': [tag_ids,],
    },
}
```

## Views
### index

### getTags
#### 作用
获取某个category下的所有tag以及tag中问题的难度分布

#### 请求
```json
{'c': 'category_name'}
```

+ `c` 所请求的category的名称

#### 响应
```json
{
    'err': {'code': num, 'msg': ['error msg']},
    'tags': [{
        'id': tag_id,
        'name': 'tag_name',
        'question_dist': [{'level': num, 'count': num},]
    }]
}
```

+ `err` 错误信息
    + 'code' 错误码
    + 'msg' 错误描述，有几条写几条
+ `tags` 返回的结果
    + `name` tag名称
    + `question_dist` 该tag中的问题难度分布
        + `level` 难度级别
        + `count` 该难度级别下的问题总数

#### 限制
category_name保存在session[ss.CATEGORY_NAME]中

### getQuestions()


