import pickle

class StockNameRecognizer(object):

    def __init__(self, stock_dict_path):
        with open(stock_dict_path, "rb") as f:
            self.stock_dict = pickle.load(f)['items']

    def recognize(self, query):

        candidate_dict_list = []
        
        query = query.upper()

        for name, info in self.stock_dict.items():
            if name in query:
                candidate_dict_list.append(info)

        if len(candidate_dict_list) < 1: 
            return None

        return candidate_dict_list
