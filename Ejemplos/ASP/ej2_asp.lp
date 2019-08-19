

nodo(a). % a es un nodo. a es una constante porque esta escrita en minuscula
nodo(b).
nodo(c).
nodo(d).
nodo(e).

% aca abajo p es una funcion de aridad 1
elemento(p(X)) :- nodo(X).

predicado(X,Y) :- nodo(X).


arco(a,b).
arco(b,c).
arco(b,d).
arco(d,e).
arco(a,a).

color_arco(a,b,azul).
color_arco(b,c,azul).
color_arco(b,d,negro).
color_arco(d,e,negro).
color_arco(a,a,negro).
%arco(juan,pedro).

%nodo(X) :- arco(X,Y).
%nodo(X) :- arco(Y,X).

%p(X) :- nodo(X).
%migomismo(X) :- nodo(X),arco(X,X).

%tiene_salida(X) :- arco(X,Y).


misterio(X,Y) :- arco(X,Z),arco(Z,Y).
% alcanzable(X,Y) : Y es alcanzable desde X
alcanzable(X,Y) :- arco(X,Y).
alcanzable(X,Y) :- alcanzable(X,Z),alcanzable(Z,Y).

%alcanzable (X,Y,C) Y es alcanzable desde X a traves de arcos de color C
alcanzable(X,Y,C) :- arco(X,Y),color_arco(X,Y,C).
alcanzable(X,Y,C) :- alcanzable(X,Z,C),alcanzable(Z,Y,C).
