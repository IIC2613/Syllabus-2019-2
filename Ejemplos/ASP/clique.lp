nodo(a).
nodo(b).
nodo(c).

arco(a,b).
arco(b,c).
arco(a,c).

unidos(X,Y) :- arco(X,Y).
unidos(X,Y) :- arco(Y,X).

% unido_con_todos(X) es verdadera cuando X esta unido
%con todos los elementos que no son X

unido_con_todos(X) :- nodo(X), not no_unido_con_todos(X).

% no_unido_con_todos(X,Y) es verdadera cuando X no esta unido
% con todos los elementos que no son X

no_unido_con_todos(X) :- nodo(Y), nodo(X), X!=Y, not unidos(X,Y).
