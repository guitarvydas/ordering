import py0d as zd
import sys

def main ():
    arg_array = zd.parse_command_line_args ()
    root_project = arg_array [0] 
    root_0D = arg_array [1]
    arg = arg_array [2]
    main_container_name = arg_array [3]
    diagram_names = arg_array [4]
    palette = zd.initialize_component_palette (root_project, root_0D, diagram_names, components_to_include_in_project)
    zd.run (palette, root_project, root_0D, arg, main_container_name, diagram_names, start_function,
              show_hierarchy=False, show_connections=False, show_traces=False, show_all_outputs=True)

def start_function (root_project, root_0D, arg, main_container):
    arg = zd.new_datum_string (f'{arg}')
    srcmsg = zd.make_message("x", arg)
    print ("injecting x")
    zd.inject (main_container, srcmsg)
    srcmsg = zd.make_message("z", arg)
    print ("injecting z")
    zd.inject (main_container, srcmsg)
    srcmsg = zd.make_message("y", arg)
    print ("injecting y")
    zd.inject (main_container, srcmsg)


## Leaf components for this project...
def components_to_include_in_project (root_project, root_0D, reg):
    zd.register_component (reg, zd.Template ( name = "1then2withoverrun", instantiator = deracer_with_overrun))
    zd.register_component (reg, zd.Template ( name = "do something", instantiator = do_something))




# Deracer_States :: enum { idle, want1, want2, wantReset }

class Deracer_Instance_Data:
    def __init__ (self, state="idle", buffer=None):
        self.state=state
        self.buffer=buffer

class TwoMessages:
    def __init__ (self, first=None, second=None):
        self.first = first
        self.second = second

def reclaim_Buffers_from_heap (inst):      
    pass  # not needed because Python does garbage collection implicitly

def deracer_with_overrun (reg, owner, name, template_data):      
    name_with_id = zd.gensym ("deracer with overrun")
    inst = Deracer_Instance_Data (buffer=TwoMessages ())
    inst.state = "idle"
    eh = zd.make_leaf (name=name_with_id, owner=owner, instance_data=inst, handler=deracer_handler)
    return eh

def send_first_then_second (eh, inst, msg):
    zd.forward (eh, "1", inst.buffer.first)
    zd.forward (eh, "2", inst.buffer.second)
    inst.state = "wantReset"

def deracer_handler (eh, msg):      
    inst = eh.instance_data
    if inst.state == "idle":
        if "1" == msg.port:
            inst.buffer.first = msg
            inst.state = "want2"
        elif "2" == msg.port:
            inst.buffer.second = msg
            inst.state = "want1"
        elif "reset" == msg.port:
            inst.state = "idle"
        else:
            zd.send (eh, "✗", f"bad msg.port (case A) for deracer {msg.port}", msg)
            inst.state = "idle"
            
    elif inst.state == "want1":
        if "1" == msg.port:
            inst.buffer.first = msg
            send_first_then_second (eh, inst, msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        elif "2" == msg.port:
            zd.send_string (eh, "✗", "overrun", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        elif "reset" == msg.port:
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        else:
            zd.send (eh, "✗", f"bad msg.port (case B) for deracer {msg.port}", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
            
    elif inst.state == "want2":
        if "2" == msg.port:
            inst.buffer.second = msg
            send_first_then_second (eh, inst, msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        elif "1" == msg.port:
            zd.send_string (eh, "✗", "overrun", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        elif "reset" == msg.port:
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        else:
            zd.send (eh, "✗", f"bad msg.port (case C) for deracer {msg.port}", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
            
    elif inst.state == "wantReset":
        if "reset" == msg.port:
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        elif "2" == msg.port:
            zd.send_string (eh, "✗", "overrun", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        elif "1" == msg.port:
            zd.send_string (eh, "✗", "overrun", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
        else:
            zd.send (eh, "✗", f"bad msg.port (case D) for deracer {msg.port}", msg)
            reclaim_Buffers_from_heap (inst)
            inst.state = "idle"
            
    else:
        zd.send (eh, "✗", f"bad state for deracer {eh.state}", msg)
        reclaim_Buffers_from_heap (inst)
        inst.state = "idle"
        
        

## Do Something                  

# states = {nothing, wanty, wantz, wantdone}
                  
class DoSomething_Instance_Data:
    def __init__ (self):
        self.state="nothing"

def do_something (reg, owner, name, template_data):      
    name_with_id = zd.gensym ("do something")
    inst = DoSomething_Instance_Data ()
    inst.state = "idle"
    eh = zd.make_leaf (name=name_with_id, owner=owner, instance_data=inst, handler=do_something_handler)
    return eh

def do_something_handler (eh, msg):      
    inst = eh.instance_data
    if inst.state == "idle":
        if "x" == msg.port:
            print ("got x")
            inst.state = "wanty"
        else:
            print (f'bad order in state idle "{msg.port}"')
            sys.exit (1)
    elif inst.state == "wanty":
        if "y" == msg.port:
            print ("got y")
            inst.state = "wantz"
        else:
            print (f'bad order in state wanty "{msg.port}"')
            sys.exit (1)
    elif inst.state == "wantz":
        if "z" == msg.port:
            print ("got z")
            print ("finished")
            zd.send (eh, "finished", zd.new_datum_bang (), msg)
            inst.state = "idle"
            sys.exit (0)
        else:
            print (f'bad order in state wantz "{msg.port}"')
            sys.exit (1)
    else:
            print (f'bad state in wantdone "{inst.state}"')
            sys.exit (1)
        

main ()
