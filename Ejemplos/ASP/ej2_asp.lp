

nodo(a). % a es un nodo. a es una constante porque esta escrita en minuscula
nodo(b).
nodo(c).
nodo(d).
nodo(e).

arco(a,b).
arco(b,c).
arco(b,d).
arco(d,e).
arco(a,a).
arco(juan,pedro).

nodo(X) :- arco(X,Y).
nodo(X) :- arco(Y,X).

%p(X) :- nodo(X).
migomismo(X) :- nodo(X),arco(X,X).

%tiene_salida(X) :- arco(X,Y).
