# py_singleton
A simple singleton helper class to inherit from.   Will check if create/close is in pair.

What I'd like to recommand most is ... *ASSERTION happens when resources leak*, e.g.
```shellscript
child = Child()
child_leaked = Child()
# Child is actually initialized only once.

child.close()
# child_leaked.close()
# Assertion happens 
```
