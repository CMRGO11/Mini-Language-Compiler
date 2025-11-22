# Mini Language Compiler  
### *Python-based educational compiler with Lexer → Parser → AST → TAC pipeline*

This project implements a simplified compiler for a small imperative language.  
It includes all major compilation stages:

- **Lexical Analysis**
- **Syntactic Analysis (Recursive Descent Parser)**
- **AST Construction**
- **Semantic Analysis (stub for future extension)**
- **TAC (Three-Address Code) Generation**
- **Simulated TAC Execution**

The repository also contains a complete **suite of 12 tests** covering declarations, assignments, arithmetic, boolean expressions, control-flow structures, semantic error cases, and integrated programs.

This compiler was developed as part of an academic assignment.

---

# 📁 Repository Structure

```
Mini-Language-Compiler/
├── run_tests.py             # Script to run all tests automatically
├── src/
│   ├── compilador.py        # Main compiler implementation
│   └── placeholder.txt
├── tests/
│   ├── basic/               # Basic test cases
│   ├── control_flow/        # If, if-else, while tests
│   ├── semantic_errors/     # Programs containing intentional semantic errors
│   └── integration/         # Full programs mixing multiple features
├── docs/
│   └── placeholder.txt
└── README.md
```

# 🛠️ How to Download and Run the Compiler

Running the compiler is very simple — you only need **Python installed** and the project folder.

Follow these steps:

---

## 📥 1. Download the Project

1. Go to the repository on GitHub  
2. Click **Code → Download ZIP**  
3. Extract the ZIP file anywhere on your computer

---

## ▶️ 2. Run the Compiler

1. Open the extracted folder  
2. Locate the file:
src/compilador.py
3. Run the file:

---

## 🧭 3. Choose What You Want to Do

When the compiler starts, this menu appears:

========================================

Bienvenido al Mini-Language Compiler

Selecciona una opción:

Cargar archivo .txt desde ruta

Ejecutar la demo (ejemplo.txt)

========================================

---

## ✔️ Option 1 — Compile Your Own `.txt` Program

## ✔️ Option 2 — Run the Demo Program

This will show:

- Tokens generated  
- AST construction  
- TAC (Three-Address Code)  
- Execution results  

---

## 🎉 Ready to Use!

Anyone can download the project and run the compiler easily in Python

# 🧠 Language Features

## 🟦 Data Types Supported
- `int`
- `bool`

## 🟩 Statements
### ✔️ Variable Declarations
```
int x;
```

### ✔️ Assignments
```
x = 10;
```

### ✔️ Print Statement
```
print(x);
```

### ✔️ If / Else
```c
if (x > 0) {
    print(1);
} else {
    print(0);
}
```

### ✔️ While Loop
```c
while (x > 0) {
    x = x - 1;
}
```

## 🟧 Expressions Supported
- Arithmetic: `+ - * /`
- Comparison: `< <= > >= == !=`
- Logical: `&& || !`
- Boolean: `true`, `false`

---

# 🔧 Compiler Pipeline (Overview)

```
Source Code
    ↓
Lexer
    ↓
Tokens
    ↓
Parser + AST Builder
    ↓
Abstract Syntax Tree (AST)
    ↓
Semantic Analyzer (stub)
    ↓
TAC Generator
    ↓
Three-Address Code (TAC)
    ↓
Simulated TAC Execution
```

---

# 🧪 Test Suite (12 Total)

## ✔️ Basic Tests (4)
Covers:
- declarations  
- assignments  
- arithmetic  
- boolean expressions  

## ✔️ Control Flow Tests (4)
Covers:
- `if`
- `if-else`
- `while`
- nested blocks

## ✔️ Semantic Error Tests (2)
Intentionally incorrect programs:
- use of undeclared variables  
- invalid type assignments  

## ✔️ Integration Tests (2)
Full programs combining:
- declarations  
- assignments  
- arithmetic  
- booleans  
- control flow  
- printing  

---



# 📘 Mini Language – Official Language Specification  
### Developed for the Mini Language Compiler (Python)

---

# 1. Overview

Mini Language is a small imperative programming language designed for educational purposes.  
Its goal is to provide a clear and simple platform to explore compiler construction techniques, including:

- Lexical analysis  
- Parsing with a recursive descent parser  
- Abstract Syntax Tree (AST) construction  
- Semantic analysis  
- Three-Address Code (TAC) generation  
- Simulated execution of TAC  

Mini Language supports variables, arithmetic expressions, boolean expressions, conditional execution, loops, and printing values.

---

# 2. Lexical Structure

Mini Language is case-sensitive.

## 2.1 Whitespace
Whitespace may appear between tokens and is ignored except for separating tokens.

## 2.2 Comments
Single-line comments begin with:

```
//
```

Everything after `//` until the end of the line is ignored.

## 2.3 Identifiers
Identifiers are sequences of letters and digits, beginning with a letter:

```
[a-zA-Z][a-zA-Z0-9]*
```

## 2.4 Keywords
Reserved keywords cannot be used as identifiers:

```
int
bool
true
false
if
else
while
print
```

## 2.5 Operators

### Arithmetic
```
+   -   *   /
```

### Comparison
```
<   <=   >   >=   ==   !=
```

### Logical
```
&&   ||   !
```

### Assignment
```
=
```

## 2.6 Punctuation
```
;   (   )   {   }
```

---

# 3. Data Types

Mini Language supports two primitive types:

- **int** — 32-bit integer  
- **bool** — Boolean (`true` or `false`)  

Variables must be declared before use.

---

# 4. Syntax (Grammar)

The grammar is written in EBNF form for clarity.

```
program         ::= { declaration | statement }

declaration     ::= type ID ";"

type            ::= "int" | "bool"

statement       ::= assignment
                  | print_stmt
                  | if_stmt
                  | while_stmt
                  | block

assignment      ::= ID "=" expression ";"

print_stmt      ::= "print" "(" expression ")" ";"

if_stmt         ::= "if" "(" expression ")" statement
                    [ "else" statement ]

while_stmt      ::= "while" "(" expression ")" statement

block           ::= "{" { statement } "}"

expression      ::= logic_or

logic_or        ::= logic_and { "||" logic_and }

logic_and       ::= equality { "&&" equality }

equality        ::= comparison { ("==" | "!=") comparison }

comparison      ::= term { ("<" | "<=" | ">" | ">=") term }

term            ::= factor { ("+" | "-") factor }

factor          ::= unary { ("*" | "/") unary }

unary           ::= "!" unary
                  | "-" unary
                  | primary

primary         ::= INT
                  | TRUE
                  | FALSE
                  | ID
                  | "(" expression ")"
```

---

# 5. Semantic Rules

Although the reference compiler includes a *semantic stub*, the full language specification defines expected semantic behavior.

### 5.1 Declaration Rules
- A variable must be declared before it is used.
- Variables cannot be redeclared in the same scope.

### 5.2 Type Checking Rules
- Arithmetic operators apply only to `int`.
- Comparison operators apply only to `int`.
- Logical operators apply only to `bool`.
- Assignment must match variable type:
  
```
int x;
x = true;   // ERROR
```

### 5.3 Boolean Semantics
- `true` and `false` are valid boolean literals.
- Boolean expressions must evaluate to either boolean literal.

### 5.4 Control Flow Conditions
- The condition of `if` and `while` must be boolean:

```
if (3) { ... }     // ERROR: condition must be bool
```

---

# 6. Runtime Behavior

Mini Language has no runtime input.  
Output is produced by the `print(expr)` statement.

```
print(x);
print(true);
```

Values are printed as:

- integers: numeric output
- booleans: `true` / `false`

---

# 7. TAC (Three-Address Code) Specification

The compiler lowers AST expressions into TAC form.  
All intermediate expressions become temporary variables:

```
t1 = x + 1
t2 = t1 * y
```

## 7.1 TAC Instructions Supported

```
assign     x := y
binary     t := a op b
unary      t := op a
goto       goto L1
if         if t == false goto L2
label      L1:
print      print x
```

## 7.2 Control Flow

If-statement:

```
t1 := condition
if t1 == false goto L1
    ... true branch ...
goto L2
L1:
    ... false branch ...
L2:
```

While-statement:

```
L1:
t1 := condition
if t1 == false goto L2
    ... body ...
goto L1
L2:
```

---

# 8. Examples

## 8.1 Basic Program

```
int x;
x = 10;
print(x);
```

TAC output:

```
x := 10
print x
```

## 8.2 If / Else

```
int x;
x = 5;

if (x > 0) {
    print(1);
} else {
    print(0);
}
```

## 8.3 While Loop

```
int x;
x = 3;

while (x > 0) {
    print(x);
    x = x - 1;
}
```

---

# 9. Compiler Pipeline

```
Source Code
    ↓
Lexer
    ↓
Tokens
    ↓
Parser
    ↓
AST
    ↓
Semantic Analyzer (stub)
    ↓
TAC Generator
    ↓
TAC Execution (simulated)
```

---

# 10. Limitations & Notes

- The semantic analyzer is currently a minimal stub and does *not* detect semantic errors.
- The runtime is simulated and does not yet execute full TAC semantics.
- No function definitions or user-defined types.
- No arrays, strings, or pointers.
- Variables are global scope only.

---

# 11. Authors
 
**Names:**
Bruno Tarango Garay (182639)

Daniel de Jesús Martínez Gallegos (179788)

Diego Bedolla Carrillo (181439)

Diego Camargo Padilla (180892)



