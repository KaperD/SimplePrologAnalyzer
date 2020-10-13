from parser import parseText
import unittest

class TestParser(unittest.TestCase):
    def test_CorrectModule(self):
        self.assertTrue(parseText('module name.'))
        self.assertTrue(parseText('module types.'))
        self.assertTrue(parseText('   module    modulo.'))
        self.assertTrue(parseText(' module\n\tgg.'))

    def test_WrongModule(self):
        self.assertFalse(parseText('Module name.'))
        self.assertFalse(parseText('module Name.'))
        self.assertFalse(parseText('module [g].'))
        self.assertFalse(parseText('module (name).'))
        self.assertFalse(parseText('module name'))
        self.assertFalse(parseText('module .'))

    def test_CorrectTypeDefs(self):
        self.assertTrue(parseText('type t a.'))
        self.assertTrue(parseText('type t a -> b.'))
        self.assertTrue(parseText('type filter (A -> o) -> list A -> list A -> o.'))
        self.assertTrue(parseText('type fruit string -> o.'))
        self.assertTrue(parseText('type t A -> (A -> B) -> (A -> C) -> (f f f f).'))

    def test_WrongTypeDefs(self):
        self.assertFalse(parseText('type t.'))
        self.assertFalse(parseText('type type type -> type.'))
        self.assertFalse(parseText('type x -> y -> z.'))
        self.assertFalse(parseText('type t A a -> b.'))
        self.assertFalse(parseText('type t A -> b -> () -> a.'))
        self.assertFalse(parseText('type t A -> B -> -> C.'))
        self.assertFalse(parseText('type A a -> b.'))
        self.assertFalse(parseText('type module a.'))
        self.assertFalse(parseText('type t a a a a a -> a _>.'))

    def test_correctRelations(self):
        self.assertTrue(parseText('f.'))
        self.assertTrue(parseText('f :- g.'))
        self.assertTrue(parseText('f :- g, h; t.'))
        self.assertTrue(parseText('f :- g, (h; t).'))
        self.assertTrue(parseText('f a :- g, h (t c d).'))
        self.assertTrue(parseText('f (cons h t) :- g h, f t.'))
        self.assertTrue(parseText('f :-    (  ( ((g))  )).'))
        self.assertTrue(parseText('odd (cons H (cons H1 T)) (cons H T1) :- odd T T1.'))
        self.assertTrue(parseText('odd (cons H nil) nil.'))
        self.assertTrue(parseText('odd nil nil.'))
        self.assertTrue(parseText('f :- (b;a),(q,w,e).'))
        self.assertTrue(parseText('g:- ((a)  ;(b),(c)   ), aa.'))
        self.assertTrue(parseText('f :- (a,     b);c;(c,b),(a,b).'))
        self.assertTrue(parseText('f f f f :- f f f f f f.'))
        self.assertTrue(parseText('f (a((f))) (a):- o (a) (a(aa a) a a a (a (a))),a,a,a;a.'))
        self.assertTrue(parseText('transition A X A :- state A, makes0 X.'))

    def test_wrongMissingDot(self):
        self.assertFalse(parseText('f'))
        self.assertFalse(parseText('f :- g'))
        self.assertFalse(parseText('f :- g, h; t'))
        self.assertFalse(parseText('f :- g, (h; t)'))
        self.assertFalse(parseText('f a :- g, h (t c d)'))
        self.assertFalse(parseText('f (cons h t) :- g h, f t'))
        self.assertFalse(parseText('f :-    (  ( ((g))  ))'))
        self.assertFalse(parseText('odd (cons H (cons H1 T)) (cons H T1) :- odd T T1'))
        self.assertFalse(parseText('odd (cons H nil) nil'))
        self.assertFalse(parseText('odd nil nil'))
        self.assertFalse(parseText('f :- (b;a),(q,w,e)'))
        self.assertFalse(parseText('g:- ((a)  ;(b),(c)   ), aa'))
        self.assertFalse(parseText('f :- (a,     b);c;(c,b),(a,b)'))
        self.assertFalse(parseText('f f f f :- f f f f f f'))
        self.assertFalse(parseText('f (a((f))) (a):- o (a) (a(aa a) a a a (a (a))),a,a,a;a'))
    
    def test_wrongBrackets(self):
        self.assertFalse(parseText('f (a.'))
        self.assertFalse(parseText('f :- g).'))
        self.assertFalse(parseText('f :- (g, (h; t).'))
        self.assertFalse(parseText('f :- g, (h; t)).'))
        self.assertFalse(parseText('f a :- g, h ((t)) c d).'))
        self.assertFalse(parseText('f (cons h t) (:- g h, f t.'))
        self.assertFalse(parseText('f :-    (   ((g))  )).'))
        self.assertFalse(parseText('odd cons H (cons H1 T)) (cons H T1) :- odd T T1.'))
        self.assertFalse(parseText('odd cons H nil) nil.'))
        self.assertFalse(parseText('odd nil ((nil))().'))
        self.assertFalse(parseText('f :- (b;a),(q,w,e.'))
        self.assertFalse(parseText('g:- ((a)  ;(b),c)   ), aa.'))
        self.assertFalse(parseText('f :- (a,     b);c;c,b),(a,b).'))
        self.assertFalse(parseText('f f f f :- f f f f) (f f.'))
        self.assertFalse(parseText('f (a((f))) (a):- o (a (a(aa a) a a a (a (a))),a,a,a;a.'))

    def test_wrongMissingHead(self):
        self.assertFalse(parseText('.'))
        self.assertFalse(parseText(' :- g.'))
        self.assertFalse(parseText(' :- g, h; t.'))
        self.assertFalse(parseText(' :- g, (h; t).'))
        self.assertFalse(parseText(':- g, h (t c d).'))
        self.assertFalse(parseText(':- g h, f t.'))
        self.assertFalse(parseText(':-    (  ( ((g))  )).'))
        self.assertFalse(parseText(' :- odd T T1.'))
        self.assertFalse(parseText(':-odd (cons H nil) nil.'))
        self.assertFalse(parseText(':-odd nil nil.'))
        self.assertFalse(parseText('f :- :-(b;a),(q,w,e).'))
        self.assertFalse(parseText(':- ((a)  ;(b),(c)   ), aa.'))
        self.assertFalse(parseText(' :- (a,     b);c;(c,b),(a,b).'))
        self.assertFalse(parseText(' :- f f f f f f.'))
        self.assertFalse(parseText(':- o (a) (a(aa a) a a a (a (a))),a,a,a;a.'))

    def test_wrongMissingPartOfBody(self):
        self.assertFalse(parseText('f :- .'))
        self.assertFalse(parseText('f :- ,g.'))
        self.assertFalse(parseText('f :- g, ; t.'))
        self.assertFalse(parseText('f :- g, ;(h; t).'))
        self.assertFalse(parseText('f a :- g, h (t c d),.'))
        self.assertFalse(parseText('f (cons h t) :- g h f t ;.'))
        self.assertFalse(parseText('f :-    (  ( ((g)) ; )).'))
        self.assertFalse(parseText('odd (cons H (cons H1 T),) (cons H T1) :- odd T T1.'))
        self.assertFalse(parseText('odd (cons H ,nil) nil.'))

    def test_wrongAtom(self):
        self.assertFalse(parseText('(f) g :- a.'))
        self.assertFalse(parseText('(f g) g :- a.'))
        self.assertFalse(parseText('a ((a) f) g :- a.'))
        self.assertFalse(parseText('g :- a ((a) a)  .'))
        self.assertFalse(parseText('g :- a (a ((a) a)) a.'))
        self.assertFalse(parseText('A g :- a.'))
        self.assertFalse(parseText('g (A b) :- a.'))
        self.assertFalse(parseText('[g] g :- a.'))
        self.assertFalse(parseText('g :- [a].'))
        self.assertFalse(parseText('g :- D [a, f].'))

    def test_wrongIlligalCharacter(self):
        self.assertFalse(parseText('(f) g ;- a.'))
        self.assertFalse(parseText('(f g) g :_ a.'))
        self.assertFalse(parseText(r'a ({a} f) g :- a.'))
        self.assertFalse(parseText('g :- a ((a) a) +'))
        self.assertFalse(parseText('g := a (a ((a) a)) a.'))
        self.assertFalse(parseText('module 3d.'))
        self.assertFalse(parseText('type t a -< b.'))
        self.assertFalse(parseText('type a w -> 1.'))
        self.assertFalse(parseText('g g :- "a".'))
        self.assertFalse(parseText('a = a.'))

    def test_correctProlog(self):
        self.assertTrue(parseText('''module name.
                                     type t A.
                                     f.'''))
        self.assertTrue(parseText('''module name.
                                     type t A.
                                     type t a -> b -> c.
                                     f.'''))
        self.assertTrue(parseText('''module name.
                                     type t A.
                                     f.
                                     g g g :- g g , g g ; g g (g).'''))
        self.assertTrue(parseText('''
                                     type t A.
                                     type t a -> b -> c.
                                     f.'''))
        self.assertTrue(parseText('''
                                     type t A.
                                     type t a -> b -> c.
                                     '''))
        self.assertTrue(parseText('''module name.
                                     f.'''))
        self.assertTrue(parseText('''module name.
                                     f.
                                     rr :- qe.
                                     q g g g g g s s (A) g [] [sdgs].'''))
        self.assertTrue(parseText('''
                                     f.
                                     rr :- qe.
                                     q g g g g g s s ((A)) g [] [sdgs].'''))

    def test_wrongProlog(self):
        self.assertFalse(parseText('''module name.
                                      module other.
                                      type t A.
                                      f.'''))
        self.assertFalse(parseText('''module name.
                                      type t A.
                                      f.
                                      type t t.'''))
        self.assertFalse(parseText('''module name.
                                      type t A.
                                      module other.
                                      f.'''))
        self.assertFalse(parseText('''
                                      type t A.
                                      f.
                                      type t B.'''))

    def test_correctLists(self):
        self.assertTrue(parseText('a [].'))
        self.assertTrue(parseText('a [a].'))
        self.assertTrue(parseText('a [a,b,c,d].'))
        self.assertTrue(parseText('a [X, Y, Z].'))
        self.assertTrue(parseText('a [a (b c), d, Z].'))
        self.assertTrue(parseText('a [[X, [H | T]] | Z].'))
        self.assertTrue(parseText('a [[[[[[]]]]]].'))
        self.assertTrue(parseText('a [[a], [b, c], [a|G], b , [aaa a a]].'))
        self.assertTrue(parseText('a [a|Gag].'))
        self.assertTrue(parseText('a [[v|B]|H].'))
        self.assertTrue(parseText('a g [X] Y :- f X Y.'))
    
    def test_wrongLists(self):
        self.assertFalse(parseText('a [, ].'))
        self.assertFalse(parseText('a [b, b.'))
        self.assertFalse(parseText('a g, g].'))
        self.assertFalse(parseText('a [z, b | S].'))
        self.assertFalse(parseText('a [f | b].'))
        self.assertFalse(parseText('a [[] , f | G].'))
        self.assertFalse(parseText('a [H | A b c].'))
        self.assertFalse(parseText('[X] Y :- f X Y.'))

        
if __name__ == '__main__':
    unittest.main()