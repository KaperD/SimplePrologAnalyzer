from parser import parseText, Prolog, List, Module, Atom, TypeDef, Type, Relation
import unittest

class TestParser(unittest.TestCase):
    def test_CorrectModule(self):
        self.assertTrue(parseText('module name.', Prolog))
        self.assertTrue(parseText('module types.', Prolog))
        self.assertTrue(parseText('   module    modulo.', Prolog))
        self.assertTrue(parseText(' module\n\tgg.', Prolog))

    def test_WrongModule(self):
        self.assertFalse(parseText('Module name.', Prolog))
        self.assertFalse(parseText('module Name.', Prolog))
        self.assertFalse(parseText('module [g].', Prolog))
        self.assertFalse(parseText('module (name).', Prolog))
        self.assertFalse(parseText('module name', Prolog))
        self.assertFalse(parseText('module .', Prolog))

    def test_CorrectTypeDefs(self):
        self.assertTrue(parseText('type t a.', Prolog))
        self.assertTrue(parseText('type t a -> b.', Prolog))
        self.assertTrue(parseText('type filter (A -> o) -> list A -> list A -> o.', Prolog))
        self.assertTrue(parseText('type fruit string -> o.', Prolog))
        self.assertTrue(parseText('type t A -> (A -> B) -> (A -> C) -> (f f f f).', Prolog))

    def test_WrongTypeDefs(self):
        self.assertFalse(parseText('type t.', Prolog))
        self.assertFalse(parseText('type type type -> type.', Prolog))
        self.assertFalse(parseText('type x -> y -> z.', Prolog))
        self.assertFalse(parseText('type t A a -> b.', Prolog))
        self.assertFalse(parseText('type t A -> b -> () -> a.', Prolog))
        self.assertFalse(parseText('type t A -> B -> -> C.', Prolog))
        self.assertFalse(parseText('type A a -> b.', Prolog))
        self.assertFalse(parseText('type module a.', Prolog))
        self.assertFalse(parseText('type t a a a a a -> a _>.', Prolog))

    def test_correctRelations(self):
        self.assertTrue(parseText('f.', Prolog))
        self.assertTrue(parseText('f :- g.', Prolog))
        self.assertTrue(parseText('f :- g, h; t.', Prolog))
        self.assertTrue(parseText('f :- g, (h; t).', Prolog))
        self.assertTrue(parseText('f a :- g, h (t c d).', Prolog))
        self.assertTrue(parseText('f (cons h t) :- g h, f t.', Prolog))
        self.assertTrue(parseText('f :-    (  ( ((g, prolog))  , prolog)).', Prolog))
        self.assertTrue(parseText('odd (cons H (cons H1 T prolog)) (cons H T1) :- odd T T1.', Prolog))
        self.assertTrue(parseText('odd (cons H nil) nil.', Prolog))
        self.assertTrue(parseText('odd nil nil.', Prolog))
        self.assertTrue(parseText('f :- (b;a),(q,w,e).', Prolog))
        self.assertTrue(parseText('g:- ((a)  ;(b),(c)   ), aa.', Prolog))
        self.assertTrue(parseText('f :- (a,     b);c;(c,b),(a,b).', Prolog))
        self.assertTrue(parseText('f f f f :- f f f f f f.', Prolog))
        self.assertTrue(parseText('f (a((f prolog))) (a):- o (a) (a(aa a) a a a (a (a prolog))),a,a,a;a.', Prolog))
        self.assertTrue(parseText('transition A X A :- state A, makes0 X.', Prolog))

    def test_wrongMissingDot(self):
        self.assertFalse(parseText('f', Prolog))
        self.assertFalse(parseText('f :- g', Prolog))
        self.assertFalse(parseText('f :- g, h; t', Prolog))
        self.assertFalse(parseText('f :- g, (h; t)', Prolog))
        self.assertFalse(parseText('f a :- g, h (t c d)', Prolog))
        self.assertFalse(parseText('f (cons h t) :- g h, f t', Prolog))
        self.assertFalse(parseText('f :-    (  ( ((g))  ))', Prolog))
        self.assertFalse(parseText('odd (cons H (cons H1 T)) (cons H T1) :- odd T T1', Prolog))
        self.assertFalse(parseText('odd (cons H nil) nil', Prolog))
        self.assertFalse(parseText('odd nil nil', Prolog))
        self.assertFalse(parseText('f :- (b;a),(q,w,e)', Prolog))
        self.assertFalse(parseText('g:- ((a)  ;(b),(c)   ), aa', Prolog))
        self.assertFalse(parseText('f :- (a,     b);c;(c,b),(a,b)', Prolog))
        self.assertFalse(parseText('f f f f :- f f f f f f', Prolog))
        self.assertFalse(parseText('f (a((f))) (a):- o (a) (a(aa a) a a a (a (a))),a,a,a;a', Prolog))
    
    def test_wrongBrackets(self):
        self.assertFalse(parseText('f (a.', Prolog))
        self.assertFalse(parseText('f :- g).', Prolog))
        self.assertFalse(parseText('f :- (g, (h; t).', Prolog))
        self.assertFalse(parseText('f :- g, (h; t)).', Prolog))
        self.assertFalse(parseText('f a :- g, h ((t)) c d).', Prolog))
        self.assertFalse(parseText('f (cons h t) (:- g h, f t.', Prolog))
        self.assertFalse(parseText('f :-    (   ((g))  )).', Prolog))
        self.assertFalse(parseText('odd cons H (cons H1 T)) (cons H T1) :- odd T T1.', Prolog))
        self.assertFalse(parseText('odd cons H nil) nil.', Prolog))
        self.assertFalse(parseText('odd nil ((nil))().', Prolog))
        self.assertFalse(parseText('f :- (b;a),(q,w,e.', Prolog))
        self.assertFalse(parseText('g:- ((a)  ;(b),c)   ), aa.', Prolog))
        self.assertFalse(parseText('f :- (a,     b);c;c,b),(a,b).', Prolog))
        self.assertFalse(parseText('f f f f :- f f f f) (f f.', Prolog))
        self.assertFalse(parseText('f (a((f))) (a):- o (a (a(aa a) a a a (a (a))),a,a,a;a.', Prolog))

    def test_wrongMissingHead(self):
        self.assertFalse(parseText('.', Prolog))
        self.assertFalse(parseText(' :- g.', Prolog))
        self.assertFalse(parseText(' :- g, h; t.', Prolog))
        self.assertFalse(parseText(' :- g, (h; t).', Prolog))
        self.assertFalse(parseText(':- g, h (t c d).', Prolog))
        self.assertFalse(parseText(':- g h, f t.', Prolog))
        self.assertFalse(parseText(':-    (  ( ((g))  )).', Prolog))
        self.assertFalse(parseText(' :- odd T T1.', Prolog))
        self.assertFalse(parseText(':-odd (cons H nil) nil.', Prolog))
        self.assertFalse(parseText(':-odd nil nil.', Prolog))
        self.assertFalse(parseText('f :- :-(b;a),(q,w,e).', Prolog))
        self.assertFalse(parseText(':- ((a)  ;(b),(c)   ), aa.', Prolog))
        self.assertFalse(parseText(' :- (a,     b);c;(c,b),(a,b).', Prolog))
        self.assertFalse(parseText(' :- f f f f f f.', Prolog))
        self.assertFalse(parseText(':- o (a) (a(aa a) a a a (a (a))),a,a,a;a.', Prolog))

    def test_wrongMissingPartOfBody(self):
        self.assertFalse(parseText('f :- .', Prolog))
        self.assertFalse(parseText('f :- ,g.', Prolog))
        self.assertFalse(parseText('f :- g, ; t.', Prolog))
        self.assertFalse(parseText('f :- g, ;(h; t).', Prolog))
        self.assertFalse(parseText('f a :- g, h (t c d),.', Prolog))
        self.assertFalse(parseText('f (cons h t) :- g h f t ;.', Prolog))
        self.assertFalse(parseText('f :-    (  ( ((g)) ; )).', Prolog))
        self.assertFalse(parseText('odd (cons H (cons H1 T),) (cons H T1) :- odd T T1.', Prolog))
        self.assertFalse(parseText('odd (cons H ,nil) nil.', Prolog))

    def test_wrongAtom(self):
        self.assertFalse(parseText('(f) g :- a.', Prolog))
        self.assertFalse(parseText('(f g) g :- a.', Prolog))
        self.assertFalse(parseText('a ((a) f) g :- a.', Prolog))
        self.assertFalse(parseText('g :- a ((a) a)  .', Prolog))
        self.assertFalse(parseText('g :- a (a ((a) a)) a.', Prolog))
        self.assertFalse(parseText('A g :- a.', Prolog))
        self.assertFalse(parseText('g (A b) :- a.', Prolog))
        self.assertFalse(parseText('[g] g :- a.', Prolog))
        self.assertFalse(parseText('g :- [a].', Prolog))
        self.assertFalse(parseText('g :- D [a, f].', Prolog))

    def test_wrongIlligalCharacter(self):
        self.assertFalse(parseText('(f) g ;- a.', Prolog))
        self.assertFalse(parseText('(f g) g :_ a.', Prolog))
        self.assertFalse(parseText(r'a ({a} f) g :- a.', Prolog))
        self.assertFalse(parseText('g :- a ((a) a) +', Prolog))
        self.assertFalse(parseText('g := a (a ((a) a)) a.', Prolog))
        self.assertFalse(parseText('module 3d.', Prolog))
        self.assertFalse(parseText('type t a -< b.', Prolog))
        self.assertFalse(parseText('type a w -> 1.', Prolog))
        self.assertFalse(parseText('g g :- "a".', Prolog))
        self.assertFalse(parseText('a = a.', Prolog))

    def test_correctProlog(self):
        self.assertTrue(parseText('''module name.
                                     type t A.
                                     f.''', Prolog))
        self.assertTrue(parseText('''module name.
                                     type t A.
                                     type t a -> b -> c.
                                     f.''', Prolog))
        self.assertTrue(parseText('''module name.
                                     type t A.
                                     f.
                                     g g g :- g g , g g ; g g (g).''', Prolog))
        self.assertTrue(parseText('''
                                     type t A.
                                     type t a -> b -> c.
                                     f.''', Prolog))
        self.assertTrue(parseText('''
                                     type t A.
                                     type t a -> b -> c.
                                     ''', Prolog))
        self.assertTrue(parseText('''module name.
                                     f.''', Prolog))
        self.assertTrue(parseText('''module name.
                                     f.
                                     rr :- qe.
                                     q g g g g g s s (A) g [] [sdgs].''', Prolog))
        self.assertTrue(parseText('''
                                     f.
                                     rr :- qe.
                                     q g g g g g s s ((a Prolog)) g [] [sdgs].''', Prolog))

    def test_wrongProlog(self):
        self.assertFalse(parseText('''module name.
                                      module other.
                                      type t A.
                                      f.''', Prolog))
        self.assertFalse(parseText('''module name.
                                      type t A.
                                      f.
                                      type t t.''', Prolog))
        self.assertFalse(parseText('''module name.
                                      type t A.
                                      module other.
                                      f.''', Prolog))
        self.assertFalse(parseText('''
                                      type t A.
                                      f.
                                      type t B.''', Prolog))

    def test_correctLists(self):
        self.assertTrue(parseText('a [].', Prolog))
        self.assertTrue(parseText('a [a].', Prolog))
        self.assertTrue(parseText('a [a,b,c,d].', Prolog))
        self.assertTrue(parseText('a [X, Y, Z].', Prolog))
        self.assertTrue(parseText('a [a (b c), d, Z].', Prolog))
        self.assertTrue(parseText('a [[X, [H | T]] | Z].', Prolog))
        self.assertTrue(parseText('a [[[[[[]]]]]].', Prolog))
        self.assertTrue(parseText('a [[a], [b, c], [a|G], b , [aaa a a]].', Prolog))
        self.assertTrue(parseText('a [a|Gag].', Prolog))
        self.assertTrue(parseText('a [[v|B]|H].', Prolog))
        self.assertTrue(parseText('a g [X] Y :- f X Y.', Prolog))
    
    def test_wrongLists(self):
        self.assertFalse(parseText('a [, ].', Prolog))
        self.assertFalse(parseText('a [b, b.', Prolog))
        self.assertFalse(parseText('a g, g].', Prolog))
        self.assertFalse(parseText('a [z, b | S].', Prolog))
        self.assertFalse(parseText('a [f | b].', Prolog))
        self.assertFalse(parseText('a [[] , f | G].', Prolog))
        self.assertFalse(parseText('a [H | A b c].', Prolog))
        self.assertFalse(parseText('[X] Y :- f X Y.', Prolog))

    def testsFromGitHub_List(self):
        self.assertTrue(parseText('[]', List))
        self.assertTrue(parseText('[a]', List))
        self.assertTrue(parseText('[A,B]', List))
        self.assertTrue(parseText('[a (b c), B, C]', List))
        self.assertTrue(parseText('[a | T]', List))
        self.assertTrue(parseText('[ [a] | T ]', List))
        self.assertTrue(parseText('[ [H | T], a ]', List))

        self.assertFalse(parseText('[a | a]', List))
        self.assertFalse(parseText('[A,B,]', List))
        self.assertFalse(parseText('[A,B', List))
        self.assertFalse(parseText('][', List))

    def testsFromGitHub_Module(self):
        self.assertTrue(parseText('module name.', Module))
        self.assertTrue(parseText('\t\nmodule\n\n  name_123.', Module))

        self.assertFalse(parseText('modulo name.', Module))
        self.assertFalse(parseText('modulename.', Module))
        self.assertFalse(parseText('mod ule name.', Module))
        self.assertFalse(parseText('module 123name.', Module))
        self.assertFalse(parseText('module name!', Module))

    def testsFromGitHub_Atom(self):
        self.assertTrue(parseText('a', Atom))
        self.assertTrue(parseText('a b c', Atom))
        self.assertTrue(parseText('a (b c)', Atom))
        self.assertTrue(parseText('a ((b c))', Atom))
        self.assertTrue(parseText('a ((b c)) d', Atom))
        self.assertTrue(parseText('a ((b c))  (d)', Atom))
        self.assertTrue(parseText('a ((b  c))  (d)', Atom))
        self.assertTrue(parseText('a ((b  c) )  ( d )', Atom))
        self.assertTrue(parseText('a((b c))(d)', Atom))

        self.assertFalse(parseText('a (a', Atom))
        self.assertFalse(parseText('X a', Atom))
        self.assertFalse(parseText('(a)', Atom))
        
    def testsFromGitHub_TypeDef(self):
        self.assertTrue(parseText('type a b.', TypeDef))
        self.assertTrue(parseText('type a b -> X.', TypeDef))
        self.assertTrue(parseText('type filter (A -> o) -> list a -> list a -> o.', TypeDef))
        self.assertTrue(parseText('type filter (A -> o) -> list A -> list A -> o.', TypeDef))
        self.assertTrue(parseText('type a (((b))).', TypeDef))
        self.assertTrue(parseText('type d a -> (((b))).', TypeDef))

        self.assertFalse(parseText('type type type -> type.', TypeDef))
        self.assertFalse(parseText('type x -> y -> z.', TypeDef))
        self.assertFalse(parseText('tupe x o.', TypeDef))

    def testsFromGitHub_Type(self):
        self.assertTrue(parseText('a', Type))
        self.assertTrue(parseText('Y -> X', Type))
        self.assertTrue(parseText('(Y -> X)', Type))
        self.assertTrue(parseText('(A -> B) -> C', Type))
        self.assertTrue(parseText('A -> B -> C', Type))
        self.assertTrue(parseText('list (list A) -> list A -> o', Type))
        self.assertTrue(parseText('pair A B -> (A -> C) -> (B -> D) -> pair C D', Type))

    def testsFromGitHub_Relation(self):
        self.assertTrue(parseText('a.', Relation))
        self.assertTrue(parseText('a b.', Relation))
        self.assertTrue(parseText('a:-a.', Relation))
        self.assertTrue(parseText('a :-a.', Relation))
        self.assertTrue(parseText('a:-a b.', Relation))
        self.assertTrue(parseText('a b:- (a b)  .', Relation))
        self.assertTrue(parseText('a b:- a;b,c.', Relation))
        self.assertTrue(parseText('a b:- a;(b,c).', Relation))
        self.assertTrue(parseText('a b:- (a;b),c.', Relation))
        self.assertTrue(parseText('a b:- a;b;c.', Relation))
        self.assertTrue(parseText('a b:- a,b,c.', Relation))
        self.assertTrue(parseText('a (b (c))  :- (a b) .', Relation))


if __name__ == '__main__':
    unittest.main()