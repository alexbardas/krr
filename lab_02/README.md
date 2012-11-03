### Summary

	Given several propositional formulas in a file (with a certain BNF syntax), 
	read them and evaluate each formula to a truth value.

	All the tasks are described in __KRR_Lab_02.pdb__

Backus-Naur Form syntax:

```
<formula> ::= "T" | "F" | <prop> | "!"<formula>
	      | <formula> <op> <formula> | "(" <formula> ")"
<prop> ::= "p" | "q" | "r" | "s" | "t" | "u" | "v"
<op> ::= "&" | "|" | "->" | "<->"
```

### How to run

`program`: python bnf.py input.txt
`tests`: python test_bnf.py
