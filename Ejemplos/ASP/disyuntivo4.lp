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

% lo de abajo no dice que pintemos todos los nodos
% porque resulta en un solo conjunto
% 1{pintado(a,rojo);pintado(a,verde);pintado(a,azul);
% pintado(b,rojo);pintado(b,verde);pintado(b,azul);
% pintado(c,rojo);pintado(c,verde);pintado(c,azul)}1

1 {pintado(N,C) : color(C),nodo(N)} 1.
