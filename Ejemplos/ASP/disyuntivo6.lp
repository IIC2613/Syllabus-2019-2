nodo(a).
nodo(b).
nodo(c).

color(rojo).
color(azul).
color(verde).

% lo de abajo es lo mismo que
% 1{pintado(a,rojo);pintado(a,verde);pintado(a,azul)}1
% 1{pintado(b,rojo);pintado(b,verde);pintado(b,azul)}1
% 1{pintado(c,rojo);pintado(c,verde);pintado(c,azul)}1

1 {pintado(N,C) : color(C)} 1 :- nodo(N).
:- pintado(N1,C1),pintado(N2,C2),N1!=N2,C1=C2.

#show pintado/2.
