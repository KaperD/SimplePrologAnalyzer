package lexer;

public class Token {
    public Token(String t, Object o, int line, int pos) {
        type = t;
        value = o;
        lineNumber = line;
        positionInLine = pos;
    }
    public String type;
    public Object value;
    public int lineNumber;
    public int positionInLine;
}
