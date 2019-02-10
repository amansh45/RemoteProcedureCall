from Interface import Interface
import inspect
import socket
import pickle
import traceback

self_ip = "10.42.0.228"
self_port = 12345
ip = "10.42.0.228"
port = 12344

class RPCHandler(object):
    pass

def generate_RPC_functions(className):
    interface_obj = Interface()
    members_list = inspect.getmembers(interface_obj, predicate=inspect.ismethod)

    for i in range(len(members_list)):
        func_name = members_list[i][0]
        func_parameters = inspect.getargspec(members_list[i][1]).args
        func_parameters = func_parameters[1:len(func_parameters)]

        def innerFunc(self, *param_list):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.connect((ip, port))
                bundle_data = {}
                stack = traceback.extract_stack()
                filename, codeline, funName, text = stack[-2]
                func_name = text.split('(')[0].split('.')[1]
                bundle_data["function_name"] = func_name
                bundle_data["function_params"] = list(param_list)
                bytes_data = pickle.dumps(bundle_data)
                s.sendall(bytes_data)
                data_rcv = s.recv(1024*1024)
                loaded_data = pickle.loads(data_rcv)
                s.close()
                return loaded_data["response"]
            except:
                return "Error in Connection with the server!"


        innerFunc.__doc__ = "docstring for innerfunctions"
        innerFunc.__name__ = func_name
        setattr(className, innerFunc.__name__, innerFunc)
        func_parameters.clear()


