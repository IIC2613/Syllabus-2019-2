planta(tomate).
planta(durazno).
planta(uva).
planta(oregano).

regador(r1).
regador(r2).
regador(r3).

% riega(R,P) el regador R riega a la planta P
riega(r1,durazno).
riega(r1,uva).
riega(r2,tomate).
riega(r3,oregano).
riega(r2,oregano).

% encendido(R): el regador R está encendido
%encendido(r1).

% regada(P) la planta P será regada
regada(P) :- riega(R,P),encendido(R).

% escriba reglas que permitan descubrir si es posible
% encender exactamente un regador que riegue a todas
% las plantas
2 {encendido(R) : regador(R) } 2.

% queremos eliminar los modelos en donde no se deduce
% que el oregano está regada
% yo no quiero que el oregano no esté regado
%:- not regada(X),planta(X).

:- not regada(oregano).
:- not regada(durazno).

% la siguiente regla no funciona como esperamos pues
% enciende todos los regadores
%1 {encendido(R) } 1 :- regador(R).

% esta regla enciende los regadores que corresponden;
% resuelve el problema pero no se refiere al predicado
% regada
%1 {encendido(R) : riega(R,oregano) } 1.


#show regada/1.
#show encendido/1.
