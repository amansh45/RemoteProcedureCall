from RPCHandler import RPCHandler
from RPCHandler import generate_RPC_functions

generate_RPC_functions(RPCHandler)

handler = RPCHandler()
result = handler.append_lists([4,5,6],[1,2,3],[7,8])
print(result)