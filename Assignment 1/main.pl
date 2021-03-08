size(9, 9).

:- [input].

% Print what is located in (X,Y)
print(X, Y) :-
    ( 
        covid(X,Y) -> write("C");
        home(X,Y) -> write("H");
        doctor(X,Y) -> write("D");
        mask(X,Y) -> write("M");
        write(".")
    ).

% func to implement print of the map
iterate(Y) :-
    write(Y), write(" "), 
    Y > 0, Yn is Y - 1, 
    iterate(Yn).

% Doule loop to go thru the map
show_map(X, Y) :-
    print(X,Y),
    ( size(Xlen, _), X < Xlen - 1, Xn is X + 1, show_map(Xn, Y));
    ( size(Xlen, _), X =:= Xlen - 1, Y > 0, Yn is Y - 1, 
    write("\n"),
    show_map(0, Yn)).

% Print map in terminal
map :- 
    size(_, Ymx),
    Y is Ymx - 1,
    show_map(0, Y).

% Genearting entities in random places
% generate_all :-
%     random_between(0,8, X1),    
%     random_between(0,8, Y1),
%     covid(X1, Y1), 

%     random_between(0,8, X1),    
%     random_between(0,8, Y1),
%     covid(X1, Y1), 

%     random_between(0,8, X1),    
%     random_between(0,8, Y1),
%     Fact = home(X1, Y1), 

%     random_between(0,8, X1),    
%     random_between(0,8, Y1),
%     Fact = actor(X1, Y1), 

%     random_between(0,8, X1),    
%     random_between(0,8, Y1),
%     Fact = doctor(X1, Y1), 

%     random_between(0,8, X1),    
%     random_between(0,8, Y1),
%     Fact = mask(X1, Y1).

% main function to generate map and show it
main :-
    % generate_all(),
    map().