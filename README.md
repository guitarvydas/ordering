# demo using 0D to ensure message order

# usage
make

# expected output
```
injecting x
injecting z
injecting y
got x
got y
got z
finished
```

Main.py sets things up, then injects 3 messages into the program. 

It sends in "x", then "z", then "y". 

The program rearranges them in order "x, "y", then "z". 

It prints the messages, then quits.

You can alter the `inject` calls in `main.py` to insert an extra "x", and, this should result in an overrun error.

It should work if you inject only one "x", one "y" and one "z" in any order. If you inject more than one of any of these, it should fail.

# files
## order.drawio
- 0D source code for this example
- open with draw.io editor (https://app.diagrams.net)
## order.drawio.json
- order.drawio transpiled to JSON
## main.py
- mainline for this example
- contains 2 components written in Python
  - "1then2withoverrun" mapped to python code "deracer_with_overrun"
  - "do something" mapped to python code "do_something"
## py0d.py
- 0D kernel written in Python
- all kernel routines needed for this example
## 0D/das2json/das2json
- transpiler for .drawio files to .drawio.json files
- MacOS only
- not needed if order.drawio.json already exists


