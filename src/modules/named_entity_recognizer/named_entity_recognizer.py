from .modules.date_time_recognizer import findDateRangePattern 
from .modules.city_recognizer import find_city 
from .modules.stock_name_recognizer import StockNameRecognizer

class NamedEntityRecognizer(object):

    def __init__(self, path_dict=None):
        self.path_dict = path_dict
        
        # initialize objects
        self.stock_name_recognizer = StockNameRecognizer(path_dict['stock_dict_path'])

    def recognize(self, query):
        
        result = { "location":None,
                    "date_time":None,
                    "stock_name":None,
                    }

        result['location'] = self.recognize_location(query)
        result['date_time'] = self.recognize_date_time(query)
        result['stock_name'] = self.recognize_stock_name(query)

        return result


    def recognize_date_time(self, query):
        result = findDateRangePattern(query)
        result = result['start'].strftime("%Y%m%d_%H%M%S")

        return result

    def recognize_location(self, query):
        result = find_city(query)
        return result

    def recognize_stock_name(self,query):
        result = self.stock_name_recognizer.recognize(query)
        return result
        

def main():
    named_entity_recognizer = NamedEntityRecognizer()
    result = named_entity_recognizer.recognize_date_time("2016년 2월 12일")
    print(result)

    result = named_entity_recognizer.recognize_date_time("내일 대구 광역시 날씨")
    print(result)

    result = named_entity_recognizer.recognize_date_time("이것은 테스트 입니다")
    print(result)
    result = named_entity_recognizer.recognize_location("내일 대구 광역시 날씨")
    print(result)

if __name__=='__main__':
    main()
