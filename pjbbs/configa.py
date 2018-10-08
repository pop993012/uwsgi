BROKER_URL = 'redis://127.0.0.1:6379/0'  # 消息代理地址
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' #任务结果存放地址
CELERY_TASK_SERIALIZER = 'json' #任务序列化与反序列化方案
CELERY_RESULT_SERIALIZER = 'json' #读取任务结果
CELERY_TASK_RESULT_EXPIRES = 24 * 60 * 60 # 任务过期时间
CELERY_ACCEPT_CONTENT = ['json'] # 指定接受的内容类型