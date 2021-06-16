:-use_module(library(clpfd)).
sudoku(Rows) :-
        length(Rows, 9),
        maplist(same_length(Rows), Rows),
        append(Rows, Vs), Vs ins 1..9,
        maplist(all_distinct, Rows),
        transpose(Rows, Columns),
        maplist(all_distinct, Columns),
        Rows = [Row1,Row2,Row3,Row4,Row5,Row6,Row7,Row8,Row9],
        squares(Row1, Row2, Row3),
        squares(Row4, Row5, Row6),
        squares(Row7, Row8, Row9).

squares([], [], []).
squares([S1,S2,S3|Ss1], [S4,S5,S6|Ss2], [S7,S8,S9|Ss3]) :-
        all_distinct([S1,S2,S3,S4,S5,S6,S7,S8,S9]),
        squares(Ss1, Ss2, Ss3).

  test :-
  S = [
        [_,4,3,_,8,_,2,5,_],
        [6,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,1,_,9,4],
        [9,_,_,_,_,4,_,7,_],
        [_,_,_,6,_,8,_,_,_],
        [_,1,_,2,_,_,_,_,3],
        [8,2,_,5,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,5],
        [_,3,4,_,9,_,7,1,_]
  ],
  sudoku(S),
  maplist(label,S),
  maplist(portray_clause,S).

/*run the code with*/ 
/*test.*/