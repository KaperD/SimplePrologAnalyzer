import parser.Parser;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import static assertions.Assertions.*;

public class Tests {
    static boolean parseFromString(Parser p, String s) throws IOException {
        return p.parseFromFile(new InputStreamReader(new ByteArrayInputStream(s.getBytes())));
    }

    static void testCorrect() throws IOException {
        Parser parser = new Parser();
        assertTrue(parseFromString(parser, "f."), 1);
        assertTrue(parseFromString(parser, "f :- g."), 2);
        assertTrue(parseFromString(parser, "f :- g, h  ; t."), 3);
        assertTrue(parseFromString(parser, "f :- g,   (h; t)."), 4);
        assertTrue(parseFromString(parser, "f :-    (  ( ((g))  ))."), 5);
        assertTrue(parseFromString(parser, "some    :- some , some ; some."), 6);
        assertTrue(parseFromString(parser, "f :- (b;a),(q,w,e)."), 7);
        assertTrue(parseFromString(parser, "g:- ((a)  ;(b),(c)   ), aa."), 8);
        assertTrue(parseFromString(parser, "f :- (a,     b);c;(c,b),(a,b)."), 9);
    }

    static void testWrongMissingDot() throws IOException {
        Parser parser = new Parser();
        assertFalse(parseFromString(parser, "f"), 1);
        assertFalse(parseFromString(parser, "f :- g"), 2);
        assertFalse(parseFromString(parser, "f :- g, h; t"), 3);
        assertFalse(parseFromString(parser, "f :- g, (h; t)"), 4);
        assertFalse(parseFromString(parser, "f :- ((((g))))"), 5);
        assertFalse(parseFromString(parser, "some :- some , some ; some"), 6);
        assertFalse(parseFromString(parser, "f :- (b;a),(q,w,e)"), 7);
        assertFalse(parseFromString(parser, "g:- ((a);(b),(c)),aa"), 8);
        assertFalse(parseFromString(parser, "f :- (a,b);c;(c,b),(a,b)"), 9);
    }

    static void testWrongBrackets() throws IOException {
        Parser parser = new Parser();
        assertFalse(parseFromString(parser, "f :- aw("), 1);
        assertFalse(parseFromString(parser, "f :- (g."), 2);
        assertFalse(parseFromString(parser, "f :- (g, (h; (t))."), 3);
        assertFalse(parseFromString(parser, "f :- g, (h; t))."), 4);
        assertFalse(parseFromString(parser, "f :- ((((g)))))."), 5);
        assertFalse(parseFromString(parser, "some :- some , some ; ()some."), 6);
        assertFalse(parseFromString(parser, "f :- (b;a),(q,w,(e)."), 7);
        assertFalse(parseFromString(parser, "g:- ((a);(b),(c)),aa.)"), 8);
        assertFalse(parseFromString(parser, "f :- (a,b);c;(c,b),(a,b)(."), 9);
    }

    static void testMissingHead() throws IOException {
        Parser parser = new Parser();
        assertFalse(parseFromString(parser, "."), 1);
        assertFalse(parseFromString(parser, ":- g."), 2);
        assertFalse(parseFromString(parser, ":- g, h; t."), 3);
        assertFalse(parseFromString(parser, " :- g, (h; t)."), 4);
        assertFalse(parseFromString(parser, " :- ((((g))))."), 5);
        assertFalse(parseFromString(parser, "():- some , some ; some."), 6);
        assertFalse(parseFromString(parser, "1:- (b;a),(q,w,e)."), 7);
        assertFalse(parseFromString(parser, ",:- ((a);(b),(c)),aa."), 8);
        assertFalse(parseFromString(parser, "; :- (a,b);c;(c,b),(a,b)."), 9);
    }

    static void testMissingPartOfBody() throws IOException {
        Parser parser = new Parser();
        assertFalse(parseFromString(parser, "f :- ,,,;;."), 1);
        assertFalse(parseFromString(parser, "f :- ."), 2);
        assertFalse(parseFromString(parser, "f :- g, h; ."), 3);
        assertFalse(parseFromString(parser, "f :- g, ( ; t)."), 4);
        assertFalse(parseFromString(parser, "f :- ((((g)))) , ."), 5);
        assertFalse(parseFromString(parser, "some :- some ,  ; some."), 6);
        assertFalse(parseFromString(parser, "f :- (b;a)(q,w,e)."), 7);
        assertFalse(parseFromString(parser, "g:- ((a)(b),(c)),."), 8);
        assertFalse(parseFromString(parser, "f :- (a,b);c(c,b),(a,b)."), 9);
    }

    public static void main(String[] args) throws IOException {
        testCorrect();
        testWrongMissingDot();
        testWrongBrackets();
        testMissingHead();
        testMissingPartOfBody();
        printResult();
    }
}
