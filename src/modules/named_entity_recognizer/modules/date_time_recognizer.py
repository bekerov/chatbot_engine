import re
from datetime import datetime, timedelta
 # regx init

          
def findDateRangePattern(query):
    
    # preprocessing
    query = preprocess(query)
    print("response: "+query)
        
    # regx pattern
    
    year_pattern = re.compile('\d+\s{0,4}년')
    month_pattern = re.compile('\d+\s{0,4}월')
    day_pattern = re.compile('\d+\s{0,4}일')
    number_pattern = re.compile('\d+')

   
    # match
    year_match = year_pattern.findall(query)
    month_match = month_pattern.findall(query)
    day_match = day_pattern.findall(query)

    
    # initialize
    year = [-1, -1]
    month = [-1, -1]
    day = [-1, -1]
    
    # match pattern
    for i, y in enumerate(year_match):
        tmp = number_pattern.search(y)
        year[i] = int(tmp.group())
        
    for i, m in enumerate(month_match):
        tmp = number_pattern.search(m)
        month[i] = int(tmp.group())
        
    for i, d in enumerate(day_match):
        tmp = number_pattern.search(d)
        day[i] = int(tmp.group())
    
    
    # postprocessing
    if year[0] == -1:
        year[0] = datetime.utcnow().year
        year[1] = datetime.utcnow().year
    
    if year[1] == -1:
        year[1] = year[0]
    
    if month[0] == -1:
        month[0] = datetime.utcnow().month
        month[1] = datetime.utcnow().month
    
    if month[1] == -1:
        month[1] = month[0]
        
    if day[0] == -1:
        day[0] = datetime.utcnow().day
        day[1] = datetime.utcnow().day
    
    if day[1] == -1:
        day[1] = day[0]
    
    start = datetime(year[0], month[0], day[0])
    end = datetime(year[1], month[1], day[1],23,59,59)

    if start > end:
        tmp = start
        start = end
        end = tmp

    result_date_range = {
        'start' : start,
        'end' :  end
    }
    print(result_date_range)
    
    return result_date_range

def preprocess(query):

    today = datetime.utcnow()
    
    # replace 올해, 작년, 재작년
    query = query.replace("올해", str(datetime.utcnow().year)+"년")
    query = query.replace("작년", str(datetime.utcnow().year-1)+"년")
    query = query.replace("재작년", str(datetime.utcnow().year-2)+"년")

    # replace 오늘, 어제, 그저께
    query = query.replace("오늘", today.strftime("%Y년 %m월 %d일"))

    delta = timedelta(days=1)
    query = query.replace("어제", (today-delta).strftime("%Y년 %m월 %d일"))

    delta = timedelta(days=2)
    query = query.replace("그저께", (today-delta).strftime("%Y년 %m월 %d일"))

    delta = timedelta(days=1)
    query = query.replace("내일", (today+delta).strftime("%Y년 %m월 %d일"))

    delta = timedelta(days=2)
    query = query.replace("모래", (today+delta).strftime("%Y년 %m월 %d일"))

    delta = timedelta(days=2)
    query = query.replace("모레", (today+delta).strftime("%Y년 %m월 %d일"))




    synonym_dictionary = { '한':1, '두':2, '세':3, '네':4, '다섯':5, '여섯':6 ,
                            '일곱':7, '여덟':8, '아홉':9, '열':10, '열한':11, '열두':12,
                            '일':1, '이':2, '삼':3, '사':4, '오':5, '육':6, '칠':7, '팔':8,
                            '구':9, '십':10, '십일':11, '십이':12,}

    date_pattern = re.compile("[ㄱ-ㅣ가-힣]{0,2}\d{0,2}\s{0,2}달")
    date_pattern_2 = re.compile("[ㄱ-ㅣ가-힣]{0,2}\d{0,2}\s{0,2}개월")

    number_pattern = re.compile('\d+')
    
    month_range_pattern = date_pattern.findall(query)
    month_range_pattern += date_pattern_2.findall(query)

    for match_pattern in month_range_pattern:

        number = number_pattern.findall(match_pattern)
        if len(number) >= 1:
            delta = relativedelta(months=1*int(number[0]))
            print(number[0])
        for kor_num, num in synonym_dictionary.items():
            if kor_num in match_pattern:
                delta = relativedelta(months=1*num)
                print(num) 

        from_to = (today-delta).strftime("%Y년 %m월 %d일")+ \
                            "에서 "+ \
                            today.strftime("%Y년 %m월 %d일")

        query = query.replace(match_pattern, from_to) 

    return query



