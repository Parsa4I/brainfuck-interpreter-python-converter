# Brainfuck Python Interpreter and Converter
Interpret and run BrainFuck codes or convert them to Python code.

## Usage

- Run through terminal:

```shell
python brainfuck.py compile|run <input_file> -o <output_file>
```

- Use in python:

```python
from brainfuck import Brainfuck2Python, BrainfuckInterpreter

# compile
bf = Brainfuck2Python("a string containing your program")
output = bf.compile()

# interpret
bf = BrainfuckInterpreter("a string containing your program")
output = bf.run()
```
