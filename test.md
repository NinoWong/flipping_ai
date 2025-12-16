一、通用消息规范
字段	字段名	是否必输	类型	描述
msgId	msgId	是	string	消息唯一 ID，用于幂等处理和消息排查（每条 MQ 消息一个唯一 ID）
traceId	traceId	是	string	全链路追踪 ID，用于把一次完整业务流程的所有消息串起来
timestamp	timestamp	是	long	消息生成时间，毫秒时间戳，用于延迟判断和排查
source	source	是	string	调用方标识，用于区分不同系统来源
bizType	bizType	是	string	业务类型，用于路由和分发，例如 CUT_QUESTION、REVIEW_VALIDATE、REVIEW_PAPER
data	data	是	object	业务数据体，不同接口结构不同，包含本次业务处理所需的全部信息

所有外部接口的 MQ 消息均采用统一结构：
{
  "msgId": "string",
  "traceId": "string",
  "timestamp": 1700000000000,
  "source": "string",
  "bizType": "string",
  "data": {}
}

二、教师切题接口（QUESTION_SEGMENTATION_TEACHER）
1. 字段说明
字段	字段名	是否必输	类型	描述
试卷 ID	paperId	是	string	试卷唯一 ID
试卷角色	paperRole	是	string	试卷角色：TEACHER 
图片列表	imageList	是	array	试卷图片列表
图片 ID	imageId	是	string	图片唯一 ID
图片地址	imageUrl	是	string	图片访问地址
图片处理后地址	processedImageUrl	否	string	预处理后试卷图片url
题目列表	questionList	否	array	切题后返回的大题信息列表
大题 ID	questionId	否	string	大题唯一 ID
题型	questionType	否	string	题目类型，如 CHOICE / FILL_IN / CALCULATION
大题号	questionNo	否	string	大题编号，如 “1”“3”
大题坐标	position	否	array	大题四点坐标 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
大题题干	question	否	string	大题题干 OCR 文本
大题作答内容	answer	否	string	大题作答 OCR 文本（当小题不存在时使用）
小题列表	subQuestionList	否	array	大题下的小题列表，可为空
小题 ID	subQuestionId	否	string	小题唯一 ID
小题号	subQuestionNo	否	string	小题编号，如 “(1)”
小题题干	subQuestion	否	string	小题题干 OCR 文本
小题题干坐标	subQuestionPosition	否	array	小题题干四点坐标
小题作答内容	answer	否	string	小题作答 OCR 文本
小题作答坐标	answerPosition	否	array	小题作答四点坐标

2.请求 JSON 示例
{
  "msgId": "uuid-001",
  "traceId": "trace-20251216-0001",
  "timestamp": 1700000000000,
  "source": "teaching-platform",
  "bizType": "QUESTION_SEGMENTATION_TEACHER",
  "data": {
    "paperId": "paper_001",
    "paperRole": "TEACHER",
    "imageList": [
      {
        "imageId": "img_001",
        "imageUrl": "http://xxx/1.jpg"
      },
      {
        "imageId": "img_002",
        "imageUrl": "http://xxx/2.jpg"
      }
    ]
  }
}
3. 返回 JSON 示例
{
  "msgId": "uuid-001",
  "traceId": "trace-20251216-0001",
  "timestamp": 1700000000000,
  "source": "teaching-platform",
  "bizType": "QUESTION_SEGMENTATION_TEACHER",
  "data": {
    "paperId": "paper_001",
    "paperRole": "TEACHER",
    "images": [
      {
        "imageId": "img_001",
        "imageUrl": "http://xxx/1.jpg",
        "processedImageUrl": "http://xxx/1_processed.jpg",
        "questionList": [
          {
            "questionId": "q_001",
            "questionType": "CHOICE",
            "questionNo": "1",
            "position": [
              [2144, 969],
              [3817, 969],
              [3817, 1123],
              [2144, 1123]
            ],
            "question": "请计算下列表达式：",
            "answer": "- 4 - 2 + 1/3 - 1 = - 7 + 1/3 = - 6 2/3",
            "subQuestionList": [
              {
                "subQuestionId": "sq_001",
                "subQuestionNo": "(1)",
                "subQuestion": "计算 -4 - 2",
                "subQuestionPosition": [
                  [2327, 1140],
                  [3145, 1140],
                  [3145, 1292],
                  [2327, 1292]
                ],
                "answer": "-6",
                "answerPosition": [
                  [2327, 1300],
                  [3145, 1300],
                  [3145, 1450],
                  [2327, 1450]
                ]
              },
              {
                "subQuestionId": "sq_002",
                "subQuestionNo": "(2)",
                "subQuestion": "计算 1/3 - 1",
                "subQuestionPosition": [
                  [3200, 1140],
                  [3700, 1140],
                  [3700, 1292],
                  [3200, 1292]
                ],
                "answer": "-2/3",
                "answerPosition": [
                  [3200, 1300],
                  [3700, 1300],
                  [3700, 1450],
                  [3200, 1450]
                ]
              }
            ]
          },
          {
            "questionId": "q_002",
            "questionType": "FILL_IN",
            "questionNo": "2",
            "position": [
              [100, 200],
              [500, 200],
              [500, 400],
              [100, 400]
            ],
            "question": "今天星期几？",
            "answer": "今天是星期一",
            "subQuestionList": []
          }
        ]
      },
      {
        "imageId": "img_002",
        "imageUrl": "http://xxx/2.jpg",
        "processedImageUrl": "http://xxx/2_processed.jpg",
        "questionList": [
          {
            "questionId": "q_003",
            "questionType": "CALCULATION",
            "questionNo": "1",
            "position": [
              [150, 100],
              [600, 100],
              [600, 400],
              [150, 400]
            ],
            "question": "计算 3 + 5",
            "answer": "8",
            "subQuestionList": []
          }
        ]
      }
    ]
  }
}

三、学生切题接口（QUESTION_SEGMENTATION_STUDENT）
1. 字段说明
字段	字段名	是否必输	类型	描述
试卷 ID	paperId	是	string	试卷唯一 ID
试卷角色	paperRole	是	string	试卷角色：STUDENT 
教师试卷	teacherPaper	是	array	教师试卷参考信息
图片列表	imageList	是	array	试卷图片列表
图片 ID	imageId	是	string	图片唯一 ID
图片地址	imageUrl	是	string	图片访问地址
图片处理后地址	processedImageUrl	否	string	预处理后试卷图片url
题目列表	questionList	否	array	切题后返回的大题信息列表
大题 ID	questionId	否	string	大题唯一 ID
题型	questionType	否	string	题目类型，如 CHOICE / FILL_IN / CALCULATION
大题号	questionNo	否	string	大题编号，如 “1”“3”
大题坐标	position	否	array	大题四点坐标 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
大题题干	question	否	string	大题题干 OCR 文本
大题作答内容	answer	否	string	大题作答 OCR 文本（当小题不存在时使用）
小题列表	subQuestionList	否	array	大题下的小题列表，可为空
小题 ID	subQuestionId	否	string	小题唯一 ID
小题号	subQuestionNo	否	string	小题编号，如 “(1)”
小题题干	subQuestion	否	string	小题题干 OCR 文本
小题题干坐标	subQuestionPosition	否	array	小题题干四点坐标
小题作答内容	answer	否	string	小题作答 OCR 文本
小题作答坐标	answerPosition	否	array	小题作答四点坐标

2. 请求 JSON 示例
{
  "msgId": "uuid-201",
  "traceId": "trace-20251216-0201",
  "timestamp": 1700000002000,
  "source": "teaching-platform",
  "bizType": "QUESTION_SEGMENTATION_STUDENT",
  "data": {
    "paperId": "paper_001",
    "paperRole": "STUDENT",
    
    "teacherPaper": [
      {
        "imageId": "img_t_001",
        "imageUrl": "http://xxx/teacher_1.jpg",
        "processedImageUrl": "http://xxx/teacher_1_processed.jpg",
        "questionList": [
          {
            "questionId": "q_001",
            "questionType": "CHOICE",
            "questionNo": "1",
            "position": [
              [2144, 969],
              [3817, 969],
              [3817, 1123],
              [2144, 1123]
            ],
            "question": "请计算下列表达式：",
            "answer": "- 4 - 2 + 1/3 - 1 = - 7 + 1/3 = - 6 2/3",
            "subQuestionList": [
              {
                "subQuestionId": "sq_001",
                "subQuestionNo": "(1)",
                "subQuestion": "计算 -4 - 2",
                "subQuestionPosition": [
                  [2327, 1140],
                  [3145, 1140],
                  [3145, 1292],
                  [2327, 1292]
                ],
                "answer": "-6",
                "answerPosition": [
                  [2327, 1300],
                  [3145, 1300],
                  [3145, 1450],
                  [2327, 1450]
                ]
              }
            ]
          }
        ]
      }
    ],

    "imageList": [
      {
        "imageId": "img_s_001",
        "imageUrl": "http://xxx/student_1.jpg"
      },
      {
        "imageId": "img_s_002",
        "imageUrl": "http://xxx/student_2.jpg"
      }
    ]
  }
}

3. 返回 JSON 示例
{
  "msgId": "uuid-301",
  "traceId": "trace-20251216-0301",
  "timestamp": 1700000003000,
  "source": "teaching-platform",
  "bizType": "QUESTION_SEGMENTATION_STUDENT",
  "data": {
    "paperId": "paper_001",
    "paperRole": "STUDENT",
    "images": [
      {
        "imageId": "img_s_001",
        "imageUrl": "http://xxx/student_1.jpg",
        "processedImageUrl": "http://xxx/student_1_processed.jpg",
        "questionList": [
          {
            "questionId": "q_001",
            "questionType": "CHOICE",
            "questionNo": "1",
            "position": [
              [2144, 969],
              [3817, 969],
              [3817, 1123],
              [2144, 1123]
            ],
            "question": "请计算下列表达式：",
            "answer": "- 4 - 2 + 1/3 - 1 = - 7 + 1/3 = - 6 2/3",
            "subQuestionList": [
              {
                "subQuestionId": "sq_001",
                "subQuestionNo": "(1)",
                "subQuestion": "计算 -4 - 2",
                "subQuestionPosition": [
                  [2327, 1140],
                  [3145, 1140],
                  [3145, 1292],
                  [2327, 1292]
                ],
                "answer": "-6",
                "answerPosition": [
                  [2327, 1300],
                  [3145, 1300],
                  [3145, 1450],
                  [2327, 1450]
                ]
              },
              {
                "subQuestionId": "sq_002",
                "subQuestionNo": "(2)",
                "subQuestion": "计算 1/3 - 1",
                "subQuestionPosition": [
                  [3200, 1140],
                  [3700, 1140],
                  [3700, 1292],
                  [3200, 1292]
                ],
                "answer": "-2/3",
                "answerPosition": [
                  [3200, 1300],
                  [3700, 1300],
                  [3700, 1450],
                  [3200, 1450]
                ]
              }
            ]
          },
          {
            "questionId": "q_002",
            "questionType": "FILL_IN",
            "questionNo": "2",
            "position": [
              [100, 200],
              [500, 200],
              [500, 400],
              [100, 400]
            ],
            "question": "今天星期几？",
            "answer": "今天是星期一",
            "subQuestionList": []
          }
        ]
      },
      {
        "imageId": "img_s_002",
        "imageUrl": "http://xxx/student_2.jpg",
        "processedImageUrl": "http://xxx/student_2_processed.jpg",
        "questionList": [
          {
            "questionId": "q_003",
            "questionType": "CALCULATION",
            "questionNo": "1",
            "position": [
              [150, 100],
              [600, 100],
              [600, 400],
              [150, 400]
            ],
            "question": "计算 3 + 5",
            "answer": "8",
            "subQuestionList": []
          }
        ]
      }
    ]
  }
}




四、批阅校验接口（REVIEW_VALIDATE）
1. 接口说明
功能：校验学生提交的试卷答案是否完整、合法
内部调用：试卷校验接口
bizType：REVIEW_VALIDATE
字段	字段名	是否必输	类型	描述
paperId	paperId	是	string	试卷 ID
studentId	studentId	是	string	学生 ID
questionList	questionList	是	array	学生答案列表
questionId	questionId	是	string	题目唯一 ID
answerImageUrl	answerImageUrl	是	string	学生答案图片 URL
valid	valid	否	boolean	校验结果，true 表示通过
errorList	errorList	否	array	校验不通过的题目或错误信息列表

2.请求 JSON 示例

{
  "msgId": "uuid-002",
  "traceId": "trace-20251216-0002",
  "timestamp": 1700000000000,
  "source": "teaching-platform",
  "bizType": "REVIEW_VALIDATE",
  "data": {
    "paperId": "paper_001",
    "studentId": "stu_001",
    "questionList": [
      {"questionId": "q_001", "answerImageUrl": "http://xxx/a1.jpg"}
    ]
  }
}

3. 返回 JSON 示例
{
  "msgId": "uuid-002",
  "traceId": "trace-20251216-0002",
  "code": 0,
  "message": "success",
  "data": {
    "paperId": "paper_001",
    "valid": true,
    "errorList": []
  }
}


五、批阅接口（REVIEW_PAPER）
1. 接口说明
功能：对学生试卷进行正式批阅
内部调用：
OCR
试题类型
姓名识别
留痕接口
语文作文批阅
英语作文批阅
普通试卷批阅
bizType：REVIEW_PAPER
字段	字段名	是否必输	类型	描述
paperId	paperId	是	string	试卷 ID
studentId	studentId	是	string	学生 ID
studentName	studentName	否	string	学生姓名，可选
imageList	imageList	是	array	试卷图片列表，用于 OCR、留痕等处理
imageId	imageId	是	string	图片唯一 ID
imageUrl	imageUrl	是	string	图片访问地址
questionList	questionList	是	array	题目列表
questionId	questionId	是	string	题目唯一 ID
questionType	questionType	是	string	题目类型，例如 CHINESE_ESSAY、CHOICE 等
score	score	否	number	批阅得分
comment	comment	否	string	批阅点评
totalScore	totalScore	否	number	试卷总分
questionResults	questionResults	否	array	每道题的批阅结果
traceUrl	traceUrl	否	string	留痕记录 URL，用于查看批阅过程
2. 请求 JSON 示例

{
  "msgId": "uuid-003",
  "traceId": "trace-20251216-0003",
  "timestamp": 1700000000000,
  "source": "teaching-platform",
  "bizType": "REVIEW_PAPER",
  "data": {
    "paperId": "paper_001",
    "studentId": "stu_001",
    "imageList": [
      {"imageId": "img_001", "imageUrl": "http://xxx/1.jpg"}
    ],
    "questionList": [
      {"questionId": "q_001", "questionType": "CHINESE_ESSAY"}
    ]
  }
}


3.返回 JSON 示例
{
  "msgId": "uuid-003",
  "traceId": "trace-20251216-0003",
  "code": 0,
  "message": "success",
  "data": {
    "paperId": "paper_001",
    "studentName": "张三",
    "totalScore": 95,
    "questionResults": [
      {
        "questionId": "q_001",
        "score": 45,
        "comment": "结构完整，立意清晰"
      }
    ],
    "traceUrl": "http://xxx/trace/record"
  }
}
