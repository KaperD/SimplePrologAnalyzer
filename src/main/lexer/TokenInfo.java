package lexer;

import java.util.function.Consumer;

public class TokenInfo {
    public TokenInfo(String n, String reg, Consumer<Token> f) {
        name = n;
        regex = reg;
        func = f;
    }
    String name;
    String regex;
    Consumer<Token> func;
}
