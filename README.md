# brainfuck-interpreter
A brainfuck interpreter written in Python

## Usage
- Run through terminal:
```
python brainfuck.py <path_to_bf_file>
```
- Use in another python script:
```python
from brainfuck import Brainfuck

bf = Brainfuck("a string containing your program")
output = bf.evaluate()
print(output)
```
