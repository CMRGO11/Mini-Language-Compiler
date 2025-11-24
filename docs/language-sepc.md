# Mini Language Specification
### Complete Language Reference for the Mini-Language Compiler

---

## 1. Language Overview

Mini Language is a small, imperative programming language designed for educational compiler construction. It supports basic programming constructs while maintaining simplicity for learning purposes.

**Key Characteristics:**
- Statically typed with type inference
- Imperative programming paradigm
- Simple memory model (global variables only)
- Educational focus on compiler pipeline demonstration

---

## 2. Lexical Specification

### 2.1 Character Set
- **Encoding**: UTF-8
- **Case Sensitivity**: Yes
- **Whitespace**: Spaces, tabs, newlines (ignored except as token separators)

### 2.2 Comments
```
c
```

// Single-line comments only
// Everything from // to end of line is ignored

### 2.3 Identifiers

**text**

```
pattern: [a-zA-Z_][a-zA-Z0-9_]*
examples: x, counter, my_var, MAX_SIZE
```

### 2.4 Keywords

| Category     | Keywords                    |
| ------------ | --------------------------- |
| Types        | `int`, `bool`           |
| Literals     | `true`, `false`         |
| Control Flow | `if`, `else`, `while` |
| I/O          | `print`                   |

### 2.5 Operators

| Category       | Operators                    | Precedence (high to low) |
| -------------- | ---------------------------- | ------------------------ |
| Unary          | `!`, `-`                 | 1                        |
| Multiplicative | `*`, `/`                 | 2                        |
| Additive       | `+`, `-`                 | 3                        |
| Relational     | `<`, `<=`, `>`, `>=` | 4                        |
| Equality       | `==`, `!=`               | 5                        |
| Logical AND    | `&&`                       | 6                        |
| Logical OR     | `\|\|`                       | 7                        |
| Assignment     | `=`                        | 8                        |

### 2.6 Punctuation

**text**

```
; ( ) { }
```

### 2.7 Literals

* **Integer** : `[0-9]+` (e.g., `0`, `42`, `100`)
* **Boolean** : `true`, `false`

---

## 3. Syntax Specification (EBNF)

**text**

```
program         = { statement } ;

statement       = declaration
                | assignment
                | print_statement
                | if_statement
                | while_statement
                | block ;

declaration     = ( "int" | "bool" ) identifier ";" ;

assignment      = identifier "=" expression ";" ;

print_statement = "print" "(" expression ")" ";" ;

if_statement    = "if" "(" expression ")" statement
                  [ "else" statement ] ;

while_statement = "while" "(" expression ")" statement ;

block           = "{" { statement } "}" ;

expression      = logical_or ;

logical_or      = logical_and { "||" logical_and } ;

logical_and     = equality { "&&" equality } ;

equality        = comparison [ ("==" | "!=") comparison ] ;

comparison      = term [ ("<" | "<=" | ">" | ">=") term ] ;

term            = factor { ("+" | "-") factor } ;

factor          = unary { ("*" | "/") unary } ;

unary           = ( "!" | "-" ) unary
                | primary ;

primary         = integer_literal
                | boolean_literal
                | identifier
                | "(" expression ")" ;

identifier      = [a-zA-Z_][a-zA-Z0-9_]* ;
integer_literal = [0-9]+ ;
boolean_literal = "true" | "false" ;
```

---

## 4. Type System

### 4.1 Supported Types

* **`int`** : 32-bit signed integers
* **`bool`** : Boolean values (`true` or `false`)

### 4.2 Type Rules

#### Variable Declarations

**c**

```
int x;        // ✓ Valid
bool flag;    // ✓ Valid
x = 10;       // ✓ Valid
flag = true;  // ✓ Valid
```

#### Type Compatibility

| Operation                  | Left Operand     | Right Operand | Result   |
| -------------------------- | ---------------- | ------------- | -------- |
| Arithmetic (`+ - * /`)   | `int`          | `int`       | `int`  |
| Relational (`< <= > >=`) | `int`          | `int`       | `bool` |
| Equality (`== !=`)       | `int`/`bool` | same type     | `bool` |
| Logical (`&& \|\| !`)      | `bool`         | `bool`      | `bool` |

#### Invalid Operations

**c**

```
int x = true;        // ✗ Type mismatch
bool b = 10;         // ✗ Type mismatch  
if (5) { ... }       // ✗ Condition must be bool
10 + true;           // ✗ Invalid operand types
```

---

## 5. Semantic Rules

### 5.1 Declaration Rules

* Variables must be declared before use
* No duplicate declarations in the same scope
* Variables are initialized to default values:
  * `int`: 0
  * `bool`: false

### 5.2 Scope Rules

* Single global scope only
* No nested scopes or block-level scoping

### 5.3 Control Flow Validity

* `if` and `while` conditions must evaluate to `bool`
* All code paths in conditionals are checked for reachability

---

## 6. Three-Address Code (TAC) Specification

### 6.1 TAC Instruction Set

| Instruction        | Format               | Description                  |
| ------------------ | -------------------- | ---------------------------- |
| Assignment         | `x := y`           | Direct assignment            |
| Binary Operation   | `t1 := x op y`     | Arithmetic/logical operation |
| Unary Operation    | `t1 := op x`       | Unary operation              |
| Conditional Jump   | `if x op y goto L` | Conditional branch           |
| Unconditional Jump | `goto L`           | Unconditional branch         |
| Label              | `L1:`              | Target for jumps             |
| Print              | `print x`          | Output value                 |

### 6.2 Temporary Variables

* Automatically generated: `t1`, `t2`, `t3`, ...
* Used for intermediate expression results
* Scope: Entire program

### 6.3 Labels

* Generated for control flow: `L1`, `L2`, `L3`, ...
* Unique within function (global scope in Mini Language)

### 6.4 Control Flow Patterns

#### If-Else Statement

**c**

```
// Source
if (x > 0) {
    y = 1;
} else {
    y = 0;
}

// TAC
t1 := x > 0
if t1 == false goto L1
    y := 1
    goto L2
L1:
    y := 0
L2:
```

#### While Loop

**c**

```
// Source
while (x > 0) {
    x = x - 1;
}

// TAC
L1:
    t1 := x > 0
    if t1 == false goto L2
    t2 := x - 1
    x := t2
    goto L1
L2:
```

---

## 7. Runtime Model

### 7.1 Memory Model

* **Global variables** : Statically allocated
* **Temporaries** : Virtual register-like storage
* **No heap allocation** or dynamic memory

### 7.2 Execution Model

* Sequential execution from first instruction
* No functions or procedure calls
* Simple I/O via `print` statements

### 7.3 Input/Output

* **Input** : None (programs are self-contained)
* **Output** : Via `print` statements only
* **Output format** :
* Integers: decimal representation
* Booleans: `true`/`false` literals

---

## 8. Complete Examples

### 8.1 Basic Program

**c**

```
// Source code
int x;
int y;
x = 10;
y = x * 2 + 5;
print(y);

// Generated TAC
x := 10
t1 := x * 2
t2 := t1 + 5
y := t2
print y

// Output
25
```

### 8.2 Conditional Logic

**c**

```
// Source code
int score;
bool passed;
score = 75;
if (score >= 60) {
    passed = true;
} else {
    passed = false;
}
print(passed);

// Generated TAC
score := 75
t1 := score >= 60
if t1 == false goto L1
    passed := true
    goto L2
L1:
    passed := false
L2:
print passed

// Output
true
```

### 8.3 Loop with Computation

**c**

```
// Source code
int n;
int sum;
n = 5;
sum = 0;
while (n > 0) {
    sum = sum + n;
    n = n - 1;
}
print(sum);

// Generated TAC
n := 5
sum := 0
L1:
    t1 := n > 0
    if t1 == false goto L2
    t2 := sum + n
    sum := t2
    t3 := n - 1
    n := t3
    goto L1
L2:
print sum

// Output
15
```

---

## 9. Compiler Implementation Notes

### 9.1 Pipeline Stages

1. **Lexical Analysis** : Regex-based tokenization
2. **Syntactic Analysis** : Recursive descent parsing
3. **AST Construction** : Builds abstract syntax tree
4. **Semantic Analysis** : Type checking and validation (stub)
5. **TAC Generation** : Three-address code emission
6. **Execution** : TAC interpreter execution

### 9.2 Error Handling

* **Lexical** : Invalid tokens, unmatched patterns
* **Syntactic** : Grammar violations, missing tokens
* **Semantic** : Type errors, undeclared variables (stub)

### 9.3 Limitations

* No function definitions or calls
* Single global scope only
* No arrays or complex data structures
* Semantic analyzer is currently minimal
* No separate compilation or modules

---

## 10. Grammar Quick Reference

### Core Productions:

* `program → statement*`
* `statement → decl | assign | print | if | while | block`
* `decl → ("int" | "bool") ID ";"`
* `assign → ID "=" expr ";"`
* `print → "print" "(" expr ")" ";"`
* `if → "if" "(" expr ")" statement ["else" statement]`
* `while → "while" "(" expr ")" statement`
* `block → "{" statement* "}"`

### Expression Precedence (high to low):

1. `primary → ID | LITERAL | "(" expr ")"`
2. `unary → ("!" | "-") unary | primary`
3. `factor → unary (("*" | "/") unary)*`
4. `term → factor (("+" | "-") factor)*`
5. `comparison → term (("<" | "<=" | ">" | ">=") term)*`
6. `equality → comparison (("==" | "!=") comparison)*`
7. `logical_and → equality ("&&" equality)*`
8. `logical_or → logical_and ("||" logical_and)*`
9. `expression → logical_or`
