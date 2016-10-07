import pickle
import os
from pprint import pprint
class ResultViewer(object):

    def __init__(self, result_dict_list):
        self.result_dict_list = result_dict_list

    def get_help_str(self):
        help_str = "="*50 +'\n'+\
                    "Result Viewer\n"+\
                    "="*50 +'\n'+\
                    "commands\n\n" +\
                    "search [target] : search [ target ]\n\n" + \
                    "top [number] : show top n \n\n" + \
                    "all : view all keyword result\n\n" + \
                    "clear : clear the terminal\n\n"+ \
                    "eval [ statement ] : eval statement\n" + \
                    "\t\t\tusable variables : result_dict_list \n\n" + \
                    "interactive : run interactive mode \n" + \
                    "\t\t\tusable variables : result_dict_list \n" + \
                    "\t\t\tusable commands : help, clear, exit, close \n\n" + \
                    "close : close program \n\n" + \
                    "exit : close program. same with 'close' command \n\n" + \
                    "="*50 +'\n'

        return help_str

    def ask(self, query):

        query = query.strip()

        
        if 'all' in query[:len('all')]:
            return self.result_dict_list
        elif 'top' in query[:len('top')]:
            num = int(query[len('top '):])
            return self.result_dict_list[:num]
        elif 'exit' in query[:len('exit')] or 'close' in query[:len('close')]:
            return -1
        elif 'clear'in query[:len('clear')] :
            return -2
        elif 'search' in query[:len('search')]:
            target = query[len('search '):]
            target = target.strip()

            data_list = self.result_dict_list
            result = []

            for data in data_list:
                for field, info in data.items():
                    #if type(info) == str:
                    if target in str(info):
                        result.append(data)

            return result

        elif 'eval' in query[:len('eval')]:
            statement = query[len('eval '):]
            statement = statement.strip()
            result_dict_list = self.result_dict_list
            
            result = eval(statement)

            return result
        elif 'interactive' in query[:len('interactive')]:

            result_dict_list = self.result_dict_list
            while True:
                try:
                    print(">> ",end ='')
                    statement = input()
                    if statement == 'exit' or statement == 'close':
                        break
                    elif statement =='help':
                        print(self.get_help_str())
                    elif statement == 'clear':
                        os.system('clear')
                        print(self.get_help_str())
                    elif '=' not in statement and len( statement.split(' ')) ==1 :
                        pprint(eval(statement))
                    else:
                        exec(statement)
                except Exception as e:
                    print(e)
            return "interactive mode finish"

        else:
            return 'wrong query'

    def run_on_terminal(self):
        os.system("clear") 
        print(self.get_help_str())

        while True:
            print("$ ", end='')
            query = input()
            result = self.ask(query)
            
            if result != -1 and result != -2:
                pprint(result)
            elif result == -2:
                os.system("clear")
                print(self.get_help_str())
            elif result == -1 :
                print("bye~")
                break
     
def main():
    # read 
    result_pickle_path = "./result/result.pickle"

    with open(result_pickle_path, "rb") as f:
        result = pickle.load(f)

    result_viewer = ResultViewer(result)
    result_viewer.run_on_terminal() 

if __name__=='__main__':
    main()
