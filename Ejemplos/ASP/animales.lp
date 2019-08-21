pajaro(tweety).
pajaro(chilly).

pinguino(chilly).

atipico(X) :- pinguino(X).
atipico(X) :- avestruz(X).

vuela(X) :- pajaro(X),not atipico(X).
