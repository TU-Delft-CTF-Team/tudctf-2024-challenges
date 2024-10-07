:- use_module(library(apply)).

is_node('C').
is_node('s').
is_node('4').
is_node('l').
is_node('3').
is_node('U').
is_node('H').
is_node('_').
is_node('m').
is_node('0').
is_node('t').
is_node('T').
is_node('r').

is_node('L', 't', 'e').
is_node('t', '{', 'u').
is_node('}', 't', 'l').
is_node('3', 't', 'r').
is_node('e', 'l', 'H').
is_node('l', '&', 'L').
is_node('t', '_', 's').
is_node('u', '3', '4').
is_node('D', 'T', 'U').
is_node('_', 't', '4').
is_node('&', 'a', '_').
is_node('a', '0', 'm').
is_node('4', '3', '_').
is_node('{', 'D', 'F').
is_node('F', 'C', 'T').

resolve_node(X, 0, Res) :- is_node(X),
    Res = node(X, none, none).
resolve_node(X, N, Res) :- is_node(X, Yc, Zc),
    M is N - 1,
    resolve_node(Yc, M, ResL),
    resolve_node(Zc, M, ResR),
    Res = node(X, ResL, ResR).

post_order(N, Result) :- post_order_rec(N, [], Result).
post_order_rec(node(X, none, none), Accum, [X|Accum]).
post_order_rec(node(X, Left, Right), Accum, [X|R2]) :- post_order_rec(Left, Accum, R1),
    post_order_rec(Right, R1, R2).

solve(Flag) :- resolve_node('}', 4, Tree),
    post_order(Tree, List),
    foldl(atom_concat, List, '', Flag).

main() :- solve(Flag), writeln(Flag).
