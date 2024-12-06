from socket import socket
from struct import calcsize, pack, unpack

INPUT_SIZE_FORMAT = ">I"


def read_variable_size(socket: socket) -> None | bytes:
    packed_input_size = socket.recv(calcsize(INPUT_SIZE_FORMAT))
    if not packed_input_size:
        return None
    input_size = unpack(INPUT_SIZE_FORMAT, packed_input_size)[0]
    input = socket.recv(input_size)
    if not input:
        return None
    return input


def write_variable_size(socket: socket, message: str) -> None:
    encoded_message = message.encode()
    socket.send(pack(INPUT_SIZE_FORMAT, len(encoded_message)))
    socket.send(encoded_message)


def command_handler(command, args, shared_data, user_id):
    print("hi")
    if command == "CREATE_MAP":
        
        description = args[0]
        rows = int(args[1])
        cols = int(args[2])
        cell_size = int(args[3])
        bg_color = args[4]
        map_id = shared_data.create(description = description, cols = cols, rows = rows, cellsize = cell_size, bgcolor = bg_color)

        return f">OK {description}"
    elif command == "ATTACH":
        map = shared_data.attach(args[0], user_id)

        return f">User with id:{args[1]} is attached to Map with id: {map.get_id()}"
    elif command == "LIST":
       return f"{shared_data.list()}"
    elif command == "CREATE_COMPONENT":
        component = shared_data.components.create(args[0])
        shared_data._objects[component.get_id()] = component
        return f">{component.get_id()} id of new component"
    elif command == "PLACE_COMPONENT":
        map = shared_data.get_map_for_user(user_id) 
        map[int((args[1]), int(args[2]))] = shared_data._objects[args[0]]
        return ">OK"
    elif command == "PLACE_CAR":
        map = shared_data.get_map_for_user(user_id)  
        map.place(shared_data._objects[args[0]], int(args[1]), int(args[2]))
        return ">OK"
    elif command == "ROTATE":
        shared_data._objects[args[0]]._rotation = args[1]
        return ">OK"
    elif command == "GET":
        map = shared_data.get_map_for_user(user_id)
        component = map[(int(args[0]), int(args[1]))]
        return f">{component.get_id()}"
    if command == "register":
        shared_data.components.register(args[0], args[1]) #need fix
    
        
    


    
        
            
        