# strings68 - Complete Setup Guide

A string-only programming language where variables are digit sequences and all operations work exclusively with strings.

## Quick Start (Without ANTLR)

The provided Python interpreter works standalone without needing ANTLR installation.

### 1. Save the Interpreter

Save the Python interpreter code as `strings68_interpreter.py`

### 2. Create a Test Program

Create `test.s68`:

```
# strings68 test program
1 = "Hello"
2 = " World"
3 = concat(1, 2)
print 3

10 = uppercase(3)
print 10

20 = "apple,banana,cherry"
21 = split(20, ",")
22 = get(21, "1")
print 22
```

### 3. Run It

```bash
python3 strings68_interpreter.py test.s68
```

## Full Setup with ANTLR (Optional)

If you want to use the ANTLR grammar for parsing:

### Installation on Ubuntu/Debian

```bash
# Install Java (required for ANTLR)
sudo apt update
sudo apt install default-jdk

# Install ANTLR4
cd /usr/local/lib
sudo curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar

# Add to .bashrc
echo 'export CLASSPATH=".:/usr/local/lib/antlr-4.13.1-complete.jar:$CLASSPATH"' >> ~/.bashrc
echo 'alias antlr4="java -jar /usr/local/lib/antlr-4.13.1-complete.jar"' >> ~/.bashrc
echo 'alias grun="java org.antlr.v4.gui.TestRig"' >> ~/.bashrc
source ~/.bashrc

# Install ANTLR Python runtime
pip3 install antlr4-python3-runtime
```

### Generate Parser from Grammar

```bash
# Save the grammar as strings68.g4
antlr4 -Dlanguage=Python3 strings68.g4

# This generates:
# - strings68Lexer.py
# - strings68Parser.py
# - strings68Listener.py
# - strings68Visitor.py
```

## Language Reference

### Variables
- All variables are digit sequences: `1`, `42`, `1984`, `314159`
- Variables hold strings only

### String Literals
```
1 = "hello world"
42 = "any text here"
```

### String Operations

**Transformations:**
```
2 = uppercase(1)      # Convert to uppercase
3 = lowercase(1)      # Convert to lowercase
4 = reverse(1)        # Reverse string
5 = length(1)         # Get length (as string!)
```

**Manipulation:**
```
3 = concat(1, 2)                    # Concatenate
4 = replace(1, "old", "new")        # Replace substring
5 = substring(1, "0", "5")          # Extract substring
```

**Pattern Matching:**
```
2 = match(1, "\\d+")                # Extract digits
3 = match(1, "[A-Z]+")              # Extract uppercase
```

**Arrays (split/get):**
```
2 = split(1, ",")                   # Split into array
3 = get(2, "0")                     # Get element at index
```

### Control Flow

**Conditionals:**
```
if 1 equals 2 then
    print "same"
else
    print "different"
endif

if 1 contains 2 then
    print "found"
endif

if 1 startswith 2 then
    print "starts with"
endif

if 1 endswith 2 then
    print "ends with"
endif
```

**Iteration:**
```
# Iterate over characters
1 = "abc"
foreach char in 1 do
    print char
endfor

# Iterate over array elements
10 = "a,b,c"
11 = split(10, ",")
foreach item in 11 do
    print item
endfor
```

### Comments
```
# This is a comment
1 = "hello"  # Comments can go anywhere
```

## Example Programs

### Hello World
```
1 = "Hello, World!"
print 1
```

### String Transformations
```
1 = "strings68"
2 = uppercase(1)
3 = reverse(2)
print 3
# Output: 86SGNIRTS
```

### CSV Processing
```
1 = "John,30,Engineer"
2 = split(1, ",")

3 = get(2, "0")
4 = get(2, "1")
5 = get(2, "2")

print 3
print 4
print 5
```

### Pattern Extraction
```
1 = "Order #12345 total: $99.99"
2 = match(1, "#\\d+")
3 = match(1, "\\$[\\d.]+")

print 2  # #12345
print 3  # $99.99
```

### Complex Example
```
# Process a list of names
1 = "alice,bob,charlie"
2 = split(1, ",")

print "Formatted names:"
foreach name in 2 do
    10 = uppercase(name)
    if 10 contains "A" then
        20 = ">>> "
        21 = concat(20, 10)
        print 21
    else
        print 10
    endif
endfor
```

## Usage Modes

### File Execution
```bash
python3 strings68_interpreter.py program.s68
```

### Interactive Mode
```bash
python3 strings68_interpreter.py
# Enter code, then Ctrl+D to execute
```

### As a Module
```python
from strings68_interpreter import Strings68Interpreter

interpreter = Strings68Interpreter()
output = interpreter.interpret("""
1 = "hello"
2 = uppercase(1)
print 2
""")

for line in output:
    print(line)
```

## Error Handling

The interpreter provides clear error messages:

```
# Undefined variable
print 999
# Error: Variable '999' not defined

# Invalid syntax
abc = "test"
# Error: Variable name must be digits: abc

# Index out of bounds
1 = split("a,b", ",")
2 = get(1, "5")
# Error: Index 5 out of bounds (length: 2)
```

## Design Philosophy

1. **String-Only**: No numeric calculations, everything is a string
2. **Digit Variables**: Variables are digit sequences for simple parsing
3. **No Reserved Words for Variables**: Since variables are only digits, all words can be keywords
4. **Explicit Operations**: All transformations are explicit function calls
5. **String-Based Indexing**: Even array indices are strings ("0", "1", "2")

## Performance Considerations

- Arrays are encoded as strings with null separators
- Pattern matching uses Python's regex engine
- No optimization - designed for simplicity and clarity

## Extending the Language

To add new operations:

1. Add to the grammar (if using ANTLR)
2. Add pattern matching in `evaluate_expression()`
3. Implement the operation

Example - adding a `trim` function:

```python
# In evaluate_expression():
if expr.startswith('trim('):
    inner = self.extract_function_arg(expr, 'trim')
    value = self.evaluate_expression(inner, loop_vars)
    return value.strip()
```

## Contributing

Possible improvements:
- String interpolation
- File I/O operations
- More string functions (trim, pad, format)
- Better error messages with line numbers
- Optimization for large string operations
- String-based functions/procedures
- Module system

## License

This is an experimental educational language. Use freely for learning and experimentation.
