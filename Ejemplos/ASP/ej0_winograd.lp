
% el bolso es un contenedor
% X es un contenedor si X es un bolso
% Si X es un bolso, entonces X es un contenedor
es_contenedor(X) :- bolso(X).

bolso(b1).
bolso(b2).

adorno(llavero).
adorno(sandwich).

mas_chico(sandwich,b2).
mas_chico(llavero,b1).

% X cabe en Y si X es mas chico que Y e Y es un 'contenedor' 
cabe(X,Y) :- mas_chico(X,Y), es_contenedor(Y).