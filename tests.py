from parser import parseText
import unittest

class TestParser(unittest.TestCase):
    def test_correct(self):
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

    def test_wrongIlligalCharacter(self):
        self.assertFalse(parseText('(f) g ;- a.'))
        self.assertFalse(parseText('(f g) g :_ a.'))
        self.assertFalse(parseText(r'a ({a} f) g :- a.'))
        self.assertFalse(parseText('g :- a ((a) a) +'))
        self.assertFalse(parseText('g := a (a ((a) a)) a.'))
        
if __name__ == '__main__':
    unittest.main()
