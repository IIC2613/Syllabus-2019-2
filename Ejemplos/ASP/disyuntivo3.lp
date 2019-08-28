nodo(a).
nodo(b).
nodo(c).

color(rojo).
color(azul).
color(verde).


% lo de abajo es lo mismo que
% 1{pintado(a,rojo);pintado(a,verde);pintado(a,azul)}1
1 {pintado(a,C) : color(C)} 1.
