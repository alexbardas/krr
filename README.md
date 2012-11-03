### List of solved problems from Knowledge Representation and Reasoning labs
The repo contains solved krr problems in python (including their full pdf assertions)

### Summary

	Given several propositional formulas in a file (with a certain BNF syntax), read them and evaluate each formula to a truth value.

	All the tasks are described in __KRR_Lab_02.pdb__

Backus-Naur Form syntax:

```
<formula> ::= "T" j "F" j <prop> j "!"<formula>
j <formula> <op> <formula> j "(" <formula> ")"
<prop> ::= "p" j "q" j "r" j "s" j "t" j "u" j "v"
<op> ::= "&" j "|" j "->" j "<->"
```

### How to run

`program`: python bnf.py input.txt
`tests`: python test_bnf.py
