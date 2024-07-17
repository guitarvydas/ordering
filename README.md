# demo using 0D to ensure message order

# usage
make

# expected output
```
... probe main.Enforce Order.?A₄: x
... probe main.Enforce Order.?C₃: z
... probe main.Enforce Order.?B₅: y

--- Outputs ---
⟪“”⦂“got x”⟫
⟪“”⦂“got y”⟫
⟪“”⦂“got z”⟫
⟪“”⦂“finished”⟫
```

Main.py sets things up, then injects one message to kick the program off.

The injected message causes Component "A" to begin.

Component "A" sends a sequence of 3 messages "x", "z", "y".

The code to do this is in `main.py`:

```
def A_handler (eh, msg):      
    zd.send_string (eh, "x", "x", msg)
    zd.send_string (eh, "z", "z", msg)
    zd.send_string (eh, "y", "y", msg)
```

The Component `Enforce Order` rearranges the messages in the expected order "x", "y", "z" then forwards them to the next Component in the chain (`B`). 

`B` is implemented in the routine `do_something_handler`. It just prints the messages as they come in in the correct orderor aborts if the order is wrong. In practice, `B` would do something more interesting, but this is just a demo of the workflow and I want to KISS.

## Fooling Around With The Code

A simple change would be to insert an extra "x" message and to watch what happens.

You can edit `main.py` to read
```
def A_handler (eh, msg):      
    zd.send_string (eh, "x", "x", msg)
    zd.send_string (eh, "x", "x", msg)
    zd.send_string (eh, "z", "z", msg)
    zd.send_string (eh, "y", "y", msg)
```
save and re-run `make`. 

This should result in an "overrun" message on the error port "✗" (that's a Unicode character, not an ASCII "x"). The error is sent by the `Enforce Order` Component and doesn't propagate to `B`. `B` never sees the extra "x" because `Enforce Order` bails out to `idle` when an overrun occurs.

In 0D, you can choose NOT to send a result. In function-based programming, you always have to send some sort of result which usually causes you to overload the meanings of results, using values like `nil` or `None`, and, causing the downstream components to do extra checking. Or, you can add workarounds to the function-based paradigm, like adding `exception` control flows (which violates the principles of structured programming).

# files
## order.drawio
- 0D source code for this example
- open with draw.io editor (https://app.diagrams.net)
## order.drawio.json
- order.drawio transpiled to JSON
## main.py
- mainline for this example
- contains 3 components written in Python
  - "1then2withoverrun" mapped to python code "deracer_with_overrun"
  - "do something" mapped to python code "do_something", mapped to "B"
  - "A" - simple component that sends 3 messages ("x", "z", "y")
## py0d.py
- 0D kernel written in Python
- all kernel routines needed for this example 
- the kernel was originally composed of separate files, but, combined into one file for simplicity in this example
- (the original files are available in https://github.com/guitarvydas/0D, if you want more detail)
## 0D/das2json/das2json
- transpiler for .drawio files to .drawio.json files
- MacOS only
- not needed if order.drawio.json already exists
- simple use of XML parser library to extract semantic details needed to create culled .JSON from .drawio diagrams
- (in the works: Python/Javascript version of this same app, using OhmJS instead of XML parsing library)


