# 🤖 SUMD Logic Validator

Hybrid Python-Prolog logic execution package.

## 🚀 Features

- **Multi-Engine Execution**: Supports PySwip (C-bindings), SWI-Prolog CLI subprocesses, or a pure-Python in-memory Prolog interpreter.
- **Interactive Logic Shell**: Run logic queries directly in your console.
- **Self-Contained Logic**: Ships with custom Prolog rulebases.

## 📦 Installation

```bash
pip install -e .
```

## 💻 Usage

To query the logic database, run:
```bash
sumd_logic_validator query "ancestor(john, marry)"
```

Or start the interactive shell:
```bash
sumd_logic_validator shell
```

## 📜 Logic Base (`logic/rules.pl`)

The package includes a logic base of family relationships:
```prolog
parent(john, mary).
parent(mary, bob).
parent(mary, alice).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
```
