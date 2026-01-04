# strings68 Shift and Rotate Operations

Visual guide to understanding shift and rotate operations on strings.

## Shift Left (shiftl)

Shifts characters to the left, **losing** characters on the left and **shortening** the string.

```
Original:  ABCDEF
           ^^^^^^

shiftl(s, "1"):
Step 1: Move left 1, lose 'A'
           BCDEF
Result:    BCDEF  (5 chars)

shiftl(s, "2"):
Step 1: Move left 2, lose 'AB'
           CDEF
Result:    CDEF   (4 chars)

shiftl(s, "3"):
Result:    DEF    (3 chars)

shiftl(s, "6"):
Result:    ""     (empty string)
```

**Use cases:**
- Removing prefixes
- Consuming characters from a stream
- String truncation from left

---

## Shift Right (shiftr)

Shifts characters to the right, **losing** characters on the right and **shortening** the string.

```
Original:  ABCDEF
           ^^^^^^

shiftr(s, "1"):
Step 1: Move right 1, lose 'F'
            ABCDE
Result:    ABCDE  (5 chars)

shiftr(s, "2"):
Step 1: Move right 2, lose 'EF'
            ABCD
Result:    ABCD   (4 chars)

shiftr(s, "3"):
Result:    ABC    (3 chars)

shiftr(s, "6"):
Result:    ""     (empty string)
```

**Use cases:**
- Removing suffixes
- Truncation from right
- Processing strings from the end

---

## Rotate Left (rotl)

Rotates characters to the left, **wrapping** characters from left to right.

```
Original:  ABCDEF
           ^^^^^^

rotl(s, "1"):
Step 1: Take 'A', move others left, append 'A'
           BCDEFA
Result:    BCDEFA

rotl(s, "2"):
Step 1: Take 'AB', move others left, append 'AB'
           CDEFAB
Result:    CDEFAB

rotl(s, "3"):
Result:    DEFABC

rotl(s, "6"):  (full rotation)
Result:    ABCDEF  (back to original!)

rotl(s, "7"):  (7 mod 6 = 1)
Result:    BCDEFA  (same as rotl 1)
```

**Use cases:**
- Caesar cipher (alphabet rotation)
- Circular buffers
- Round-robin scheduling
- String permutations

---

## Rotate Right (rotr)

Rotates characters to the right, **wrapping** characters from right to left.

```
Original:  ABCDEF
           ^^^^^^

rotr(s, "1"):
Step 1: Take 'F', move others right, prepend 'F'
           FABCDE
Result:    FABCDE

rotr(s, "2"):
Step 1: Take 'EF', move others right, prepend 'EF'
           EFABCD
Result:    EFABCD

rotr(s, "3"):
Result:    DEFABC

rotr(s, "6"):  (full rotation)
Result:    ABCDEF  (back to original!)
```

**Use cases:**
- Reverse Caesar cipher
- Circular queue operations
- Cyclic patterns
- Undo rotate left

---

## Key Differences

| Operation | Loses Data? | Wraps Around? | Changes Length? |
|-----------|-------------|---------------|-----------------|
| shiftl    | ✅ Yes (left)  | ❌ No | ✅ Yes (shorter) |
| shiftr    | ✅ Yes (right) | ❌ No | ✅ Yes (shorter) |
| rotl      | ❌ No | ✅ Yes | ❌ No |
| rotr      | ❌ No | ✅ Yes | ❌ No |

---

## Mathematical Properties

### Rotation Properties:
```
rotl(rotl(s, "n"), "m") = rotl(s, "n+m")
rotr(rotr(s, "n"), "m") = rotr(s, "n+m")
rotl(s, "n") = rotr(s, "length - n")
rotl(s, "length") = s
rotr(s, "length") = s
```

### Examples:
```
s = "ABCDEF" (length 6)

rotl(s, "2") = "CDEFAB"
rotr(s, "4") = "CDEFAB"  (same! because 6-4=2)

rotl(s, "8") = rotl(s, "2")  (8 mod 6 = 2)
```

---

## Practical Examples

### Caesar Cipher (ROT13):
```
1 = "HELLO"
2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
3 = rotl(2, "13")
# Now use 3 as cipher alphabet
```

### Circular Buffer:
```
1 = "12345"
2 = rotl(1, "1")  # Next position: "23451"
3 = rotl(2, "1")  # Next position: "34512"
4 = rotl(3, "1")  # Next position: "45123"
```

### Removing Processed Data:
```
1 = "QUEUE_DATA"
2 = shiftl(1, "6")  # Remove "QUEUE_", result: "DATA"
```

### Truncate from right:
```
1 = "ABCDEF"
2 = shiftr(1, "2")  # Remove last 2 chars, result: "ABCD"
```

---

## strings68 Syntax

```
# Shift operations (lose data, add spaces)
2 = shiftl(1, "2")    # Shift string in var 1 left by 2 positions
3 = shiftr(1, "3")    # Shift string in var 1 right by 3 positions

# Rotate operations (preserve data, wrap around)
4 = rotl(1, "2")      # Rotate string in var 1 left by 2 positions
5 = rotr(1, "3")      # Rotate string in var 1 right by 3 positions
```

**Note:** All position arguments are strings (e.g., "2", "3") not numbers, following the strings68 philosophy.

---

## Performance Considerations

All operations are O(n) where n is the string length:
- **Shift**: Creates new string with slicing
- **Rotate**: Creates new string with slicing and concatenation
- **Modulo**: Position % length handles over-rotation automatically

---

## Error Handling

- Empty strings: All operations return empty string
- Position 0: Returns original string unchanged
- Position > length: Automatically reduced via modulo operation
- Negative positions: Not supported (positions must be string representations of positive integers)
