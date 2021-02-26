fieldSize(9, 9).

covid(7, 2).
covid(2, 4).
home(1,1).
actor(1,8).
doctor(4,4).
mask(8,8).  % to debug


print(X, Y) :-
    ( 
        covid(X,Y) -> write("C");
        home(X,Y) -> write("H");
        doctor(X,Y) -> write("D");
        mask(X,Y) -> write("M");
        write(".")
    ).


iterate(X, Y) :-
    % format("~a ~a\n", [X, Y]),
    print(X,Y),
    ( fieldSize(XSize, _), X < XSize - 1, Xnew is X + 1, iterate(Xnew, Y));

    (fieldSize(XSize, _), X =:= XSize - 1, Y > 0, Ynew is Y - 1, 
    write("\n"),
    iterate(0, Ynew)).

iterate(Y) :-
    write(Y), write(" "), 
    Y > 0, Ynew is Y - 1, 
    iterate(Ynew).

map :- 
    fieldSize(_, YMax),
    Y is YMax - 1,
    iterate(0,Y).
