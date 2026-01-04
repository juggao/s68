#!/usr/bin/env python3
"""
strings68 Interpreter
A string-only programming language where variables are digit sequences.

Usage:
    python strings68_interpreter.py program.txt
    
Or use interactively:
    python strings68_interpreter.py
"""

import sys
import re
from typing import Dict, Any, List, Optional


# Enable debug mode by uncommenting:
# DEBUG = True
DEBUG = False

def debug_print(msg):
    """Print debug messages if DEBUG is enabled."""
    if DEBUG:
        print(f"DEBUG: {msg}", file=sys.stderr)


class Strings68Interpreter:
    """Interpreter for the strings68 language."""
    
    def __init__(self):
        self.variables: Dict[str, str] = {}
        self.output: List[str] = []
        
    def interpret(self, code: str) -> List[str]:
        """Interpret strings68 code and return output."""
        self.output = []
        lines = code.split('\n')
        self.execute_block(lines, 0, len(lines))
        return self.output
    
    def execute_block(self, lines: List[str], start: int, end: int, 
                     loop_vars: Optional[Dict[str, str]] = None) -> int:
        """Execute a block of code from start to end index."""
        if loop_vars is None:
            loop_vars = {}
            
        i = start
        while i < end:
            line = lines[i].strip()
            i += 1
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Print statement
            if line.startswith('print '):
                self.handle_print(line, loop_vars)
                continue
            
            # If statement
            if line.startswith('if '):
                i = self.handle_if(lines, i - 1, end, loop_vars)
                continue
            
            # Foreach loop
            if line.startswith('foreach '):
                i = self.handle_foreach(lines, i - 1, end, loop_vars)
                continue
            
            # While loop
            if line.startswith('while '):
                i = self.handle_while(lines, i - 1, end, loop_vars)
                continue
            
            # Assignment
            if '=' in line:
                self.handle_assignment(line, loop_vars)
                continue
        
        return i
    
    def handle_print(self, line: str, loop_vars: Dict[str, str]):
        """Handle print statements."""
        rest = line[6:].strip()
        
        # String literal
        if rest.startswith('"') and rest.endswith('"'):
            self.output.append(rest[1:-1])
        # Variable
        else:
            value = self.get_variable(rest, loop_vars)
            # Even empty strings should be printed
            self.output.append(value if value else "")
    
    def handle_assignment(self, line: str, loop_vars: Dict[str, str]):
        """Handle variable assignments."""
        parts = line.split('=', 1)
        if len(parts) != 2:
            raise SyntaxError(f"Invalid assignment: {line}")
        
        var_name = parts[0].strip()
        expr = parts[1].strip()
        
        if not re.match(r'^\d+$', var_name):
            raise SyntaxError(f"Variable name must be digits: {var_name}")
        
        value = self.evaluate_expression(expr, loop_vars)
        self.variables[var_name] = value
    
    def evaluate_expression(self, expr: str, loop_vars: Dict[str, str]) -> str:
        """Evaluate a string expression."""
        expr = expr.strip()
        
        # String literal
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        
        # Function calls
        # uppercase(...)
        if expr.startswith('uppercase('):
            inner = self.extract_function_arg(expr, 'uppercase')
            value = self.evaluate_expression(inner, loop_vars)
            return value.upper()
        
        # lowercase(...)
        if expr.startswith('lowercase('):
            inner = self.extract_function_arg(expr, 'lowercase')
            value = self.evaluate_expression(inner, loop_vars)
            return value.lower()
        
        # reverse(...)
        if expr.startswith('reverse('):
            inner = self.extract_function_arg(expr, 'reverse')
            value = self.evaluate_expression(inner, loop_vars)
            return value[::-1]
        
        # length(...)
        if expr.startswith('length('):
            inner = self.extract_function_arg(expr, 'length')
            value = self.evaluate_expression(inner, loop_vars)
            return str(len(value))
        
        # concat(arg1, arg2)
        if expr.startswith('concat('):
            args = self.extract_function_args(expr, 'concat', 2)
            val1 = self.evaluate_expression(args[0], loop_vars)
            val2 = self.evaluate_expression(args[1], loop_vars)
            return val1 + val2
        
        # split(string, delimiter)
        if expr.startswith('split('):
            args = self.extract_function_args(expr, 'split', 2)
            string_val = self.evaluate_expression(args[0], loop_vars)
            delimiter = args[1].strip('"')
            
            if delimiter == '':
                parts = list(string_val)
            else:
                parts = string_val.split(delimiter)
            
            # Encode as: length\x00part1\x00part2\x00...
            return str(len(parts)) + '\x00' + '\x00'.join(parts)
        
        # get(array, index)
        if expr.startswith('get('):
            args = self.extract_function_args(expr, 'get', 2)
            array_val = self.evaluate_expression(args[0], loop_vars)
            index_str = args[1].strip('"')
            
            parts = array_val.split('\x00')
            length = int(parts[0])
            index = int(index_str)
            
            if index < 0 or index >= length:
                raise IndexError(f"Index {index} out of bounds (length: {length})")
            
            return parts[index + 1]
        
        # match(string, pattern)
        if expr.startswith('match('):
            args = self.extract_function_args(expr, 'match', 2)
            string_val = self.evaluate_expression(args[0], loop_vars)
            pattern = args[1].strip('"')
            
            debug_print(f"Match: pattern='{pattern}' against='{string_val}'")
            
            try:
                match = re.search(pattern, string_val)
                result = match.group(0) if match else ""
                debug_print(f"Match result: '{result}'")
                return result
            except re.error as e:
                raise SyntaxError(f"Invalid regex pattern '{pattern}': {e}")
        
        # replace(string, old, new)
        if expr.startswith('replace('):
            args = self.extract_function_args(expr, 'replace', 3)
            string_val = self.evaluate_expression(args[0], loop_vars)
            old = args[1].strip('"')
            new = args[2].strip('"')
            return string_val.replace(old, new)
        
        # substring(string, start, length)
        if expr.startswith('substring('):
            args = self.extract_function_args(expr, 'substring', 3)
            string_val = self.evaluate_expression(args[0], loop_vars)
            start = int(args[1].strip('"'))
            length = int(args[2].strip('"'))
            return string_val[start:start + length]
        
        # Variable reference
        return self.get_variable(expr, loop_vars)
    
    def get_variable(self, name: str, loop_vars: Dict[str, str]) -> str:
        """Get variable value, checking loop vars first."""
        if name in loop_vars:
            return loop_vars[name]
        if name in self.variables:
            return self.variables[name]
        raise NameError(f"Variable '{name}' not defined")
    
    def extract_function_arg(self, expr: str, func_name: str) -> str:
        """Extract single function argument."""
        start = len(func_name) + 1
        end = expr.rfind(')')
        return expr[start:end].strip()
    
    def extract_function_args(self, expr: str, func_name: str, 
                            expected_count: int) -> List[str]:
        """Extract multiple function arguments."""
        start = len(func_name) + 1
        end = expr.rfind(')')
        args_str = expr[start:end]
        
        # Simple comma split (doesn't handle nested functions perfectly)
        args = []
        current = ""
        depth = 0
        in_string = False
        
        for char in args_str:
            if char == '"' and (not current or current[-1] != '\\'):
                in_string = not in_string
            elif char == '(' and not in_string:
                depth += 1
            elif char == ')' and not in_string:
                depth -= 1
            elif char == ',' and depth == 0 and not in_string:
                args.append(current.strip())
                current = ""
                continue
            
            current += char
        
        if current:
            args.append(current.strip())
        
        if len(args) != expected_count:
            raise SyntaxError(
                f"{func_name} expects {expected_count} arguments, "
                f"got {len(args)}"
            )
        
        return args
    
    def handle_if(self, lines: List[str], start: int, end: int,
                  loop_vars: Dict[str, str]) -> int:
        """Handle if statements."""
        line = lines[start].strip()
        
        # Parse condition - allow variables and string literals
        match = re.match(
            r'if\s+(\w+)\s+(equals|contains|startswith|endswith)\s+(.+?)\s+then',
            line
        )
        if not match:
            raise SyntaxError(f"Invalid if statement: {line}")
        
        var1, op, var2_expr = match.groups()
        val1 = self.get_variable(var1, loop_vars)
        
        # Check if var2 is a string literal or variable
        var2_expr = var2_expr.strip()
        if var2_expr.startswith('"') and var2_expr.endswith('"'):
            val2 = var2_expr[1:-1]  # String literal
        else:
            val2 = self.get_variable(var2_expr, loop_vars)  # Variable
        
        # Evaluate condition
        if op == 'equals':
            condition = val1 == val2
        elif op == 'contains':
            condition = val2 in val1
        elif op == 'startswith':
            condition = val1.startswith(val2)
        elif op == 'endswith':
            condition = val1.endswith(val2)
        else:
            condition = False
        
        # Find else and endif
        i = start + 1
        depth = 1
        else_pos = None
        endif_pos = None
        
        while i < end and depth > 0:
            line = lines[i].strip()
            if line.startswith('if '):
                depth += 1
            elif line == 'endif':
                depth -= 1
                if depth == 0:
                    endif_pos = i
            elif line == 'else' and depth == 1:
                else_pos = i
            i += 1
        
        if endif_pos is None:
            raise SyntaxError("Unmatched if/endif")
        
        # Execute appropriate branch
        if condition:
            exec_end = else_pos if else_pos else endif_pos
            self.execute_block(lines, start + 1, exec_end, loop_vars)
        elif else_pos:
            self.execute_block(lines, else_pos + 1, endif_pos, loop_vars)
        
        return endif_pos + 1
    
    def handle_foreach(self, lines: List[str], start: int, end: int,
                      loop_vars: Dict[str, str]) -> int:
        """Handle foreach loops."""
        line = lines[start].strip()
        
        # Parse foreach
        match = re.match(r'foreach\s+(\w+)\s+in\s+(\d+)\s+do', line)
        if not match:
            raise SyntaxError(f"Invalid foreach statement: {line}")
        
        iter_var, source_var = match.groups()
        source_value = self.get_variable(source_var, loop_vars)
        
        # Find endfor
        i = start + 1
        depth = 1
        endfor_pos = None
        
        while i < end and depth > 0:
            check_line = lines[i].strip()
            if check_line.startswith('foreach '):
                depth += 1
            elif check_line == 'endfor':
                depth -= 1
                if depth == 0:
                    endfor_pos = i
            i += 1
        
        if endfor_pos is None:
            raise SyntaxError("Unmatched foreach/endfor")
        
        # Iterate
        if '\x00' in source_value:
            # It's an array
            parts = source_value.split('\x00')
            length = int(parts[0])
            for idx in range(length):
                new_loop_vars = loop_vars.copy()
                new_loop_vars[iter_var] = parts[idx + 1]
                self.execute_block(lines, start + 1, endfor_pos, new_loop_vars)
        else:
            # It's a string - iterate characters
            for char in source_value:
                new_loop_vars = loop_vars.copy()
                new_loop_vars[iter_var] = char
                self.execute_block(lines, start + 1, endfor_pos, new_loop_vars)
        
        return endfor_pos + 1


    def handle_while(self, lines: List[str], start: int, end: int,
                     loop_vars: Dict[str, str]) -> int:
        """Handle while loops."""
        line = lines[start].strip()
        
        # Parse while
        match = re.match(
            r'while\s+(\w+)\s+(equals|contains|startswith|endswith)\s+(.+?)\s+do',
            line
        )
        if not match:
            raise SyntaxError(f"Invalid while statement: {line}")
        
        var1, op, var2_expr = match.groups()
        
        # Find endwhile
        i = start + 1
        depth = 1
        endwhile_pos = None
        
        while i < end and depth > 0:
            check_line = lines[i].strip()
            if check_line.startswith('while '):
                depth += 1
            elif check_line == 'endwhile':
                depth -= 1
                if depth == 0:
                    endwhile_pos = i
            i += 1
        
        if endwhile_pos is None:
            raise SyntaxError("Unmatched while/endwhile")
        
        # Execute loop while condition is true
        max_iterations = 10000  # Prevent infinite loops
        iterations = 0
        
        while iterations < max_iterations:
            # Evaluate condition
            val1 = self.get_variable(var1, loop_vars)
            
            # Check if var2 is a string literal or variable
            var2_expr_stripped = var2_expr.strip()
            if var2_expr_stripped.startswith('"') and var2_expr_stripped.endswith('"'):
                val2 = var2_expr_stripped[1:-1]
            else:
                val2 = self.get_variable(var2_expr_stripped, loop_vars)
            
            # Check condition
            condition = False
            if op == 'equals':
                condition = val1 == val2
            elif op == 'contains':
                condition = val2 in val1
            elif op == 'startswith':
                condition = val1.startswith(val2)
            elif op == 'endswith':
                condition = val1.endswith(val2)
            
            if not condition:
                break
            
            # Execute loop body
            self.execute_block(lines, start + 1, endwhile_pos, loop_vars)
            iterations += 1
        
        if iterations >= max_iterations:
            raise RuntimeError("While loop exceeded maximum iterations (10000)")
        
        return endwhile_pos + 1


def main():
    """Main entry point."""
    interpreter = Strings68Interpreter()
    
    if len(sys.argv) > 1:
        # Read from file
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                code = f.read()
            output = interpreter.interpret(code)
            for line in output:
                print(line)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Interactive mode
        print("strings68 Interpreter v0.1")
        print("Enter code (Ctrl+D or 'exit' to run):")
        print()
        
        lines = []
        try:
            while True:
                line = input()
                if line.strip() == 'exit':
                    break
                lines.append(line)
        except EOFError:
            pass
        
        if lines:
            code = '\n'.join(lines)
            try:
                output = interpreter.interpret(code)
                print("\n=== Output ===")
                for line in output:
                    print(line)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
