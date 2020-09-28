package parser;

import java.awt.*;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import lexer.*;
import svgDraw.*;

public class Parser {
    /*
    Prolog = Relation Prolog | Relation
    Relation = Literal :- Body | Literal .
    Body = Expression .
    Expression = Cap ; Expression | Cap
    Cap = Literal , Cap | (Expression) , Cap | Literal | (Expression)
    Literal = [a-zA-Z_][a-zA-Z_0-9]*
     */
    
    static class SyntaxError extends RuntimeException {
        SyntaxError() {}
        SyntaxError(String errorMessage) {
            super(errorMessage);
        }
    }

    static class Node {
        Node(Node l, Node r, String n) {
            left = l;
            right = r;
            name = n;
        }

        @Override
        public String toString() {
            StringBuilder s = new StringBuilder();
            s.append("(");
            if (left != null) s.append(left.toString()).append(" ");
            s.append(name);
            if (right != null) s.append(" ").append(right.toString());
            s.append(")");
            return s.toString();
        }

        Node left;
        Node right;
        String name;
    }

    boolean accept(String s) {
        if (!(current == null) && current.value.toString().equals(s)) {
            current = lexer.nextToken();
            return true;
        }
        return false;
    }

    void expect(String s) {
        String caller = Thread.currentThread().getStackTrace()[2].toString();
        if (accept(s)) {
            return;
        }
        if (current != null) {
            String error = String.format("Line %d column %d: Expected '%s' by %s, but found '%s'\n",
                    current.lineNumber, current.positionInLine + 1, s, caller, current.value.toString()) +
                    lexer.getCurrentLine() + "\n" +
                    "-".repeat(current.positionInLine) +
                    "^";
            throw new SyntaxError(error);
        } else {
            String lastLine = lexer.getCurrentLine();
            String error = String.format("Line %d column %d: Expected '%s' by %s, but nothing found\n",
                    lexer.getLineNumber(), lastLine.length(), s, caller) +
                    lexer.getCurrentLine() + "\n" +
                    "-".repeat(lastLine.length()) +
                    "^";
            throw new SyntaxError(error);
        }
    }

    Node identifier() {
        Token l = current;
        current = lexer.nextToken();
        String caller = Thread.currentThread().getStackTrace()[2].toString();
        if (l == null) {
            String lastLine = lexer.getCurrentLine();
            String error = String.format("Line %d column %d: Expected identifier by %s, but nothing found\n",
                    lexer.getLineNumber(), lastLine.length(), caller) +
                    lexer.getCurrentLine() + "\n" +
                    "-".repeat(lastLine.length()) +
                    "^";
            throw new SyntaxError(error);
        }
        if (!l.type.equals("IDENTIFIER")) {
            String error = String.format("Line %d column %d: Expected identifier by %s, but found '%s'\n",
                    l.lineNumber, l.positionInLine + 1, caller, l.value.toString()) +
                    lexer.getCurrentLine() + "\n" +
                    "-".repeat(l.positionInLine) +
                    "^";
            throw new SyntaxError(error);
        }
        return new Node(null, null, l.value.toString());
    }

    boolean isNextIdentifier() {
        Token l = current;
        if (l == null) {
            return false;
        }
        if (!l.type.equals("IDENTIFIER")) {
            return false;
        }
        return true;
    }

    ArrayList<Node> prolog() {
        ArrayList<Node> ret = new ArrayList<>();
        while (current != null) {
            Node r = relation();
            ret.add(r);
        }
        return ret;
    }

    Node relation() {
        Node l = identifier();
        if (accept(":-")) {
            Node r = body();
            return new Node(l, r, ":-");
        }
        expect(".");
        return new Node(l, new Node(null, null, "."), "");
    }

    Node body() {
        Node l = expression();
        expect(".");
        return new Node(l, new Node(null, null, "."), "");
    }

    Node expression() {
        Node l = cap();
        if (accept(";")) {
            Node r = expression();
            return new Node(l, r, ";");
        }
        return l;
    }

    Node cap() {
        Node l = null;
        if (isNextIdentifier()) {
            l = identifier();
        } else {
            if (accept("(")) {
                l = expression();
                expect(")");
            } else {
                expect("identifier or (");
            }
        }
        if (accept(",")) {
            Node r = cap();
            return new Node(l, r, ",");
        }
        return l;
    }

    int getTreeHeight(Node n) {
        int res = 0;
        if (n.left != null) res = Math.max(res, getTreeHeight(n.left));
        if (n.right != null) res = Math.max(res, getTreeHeight(n.right));
        return res + 1;
    }

    void drawTreeToSvg(Node n, int x, int y, int l, int r) {
        int myX = (l + r) / 2;
        int myY = y + 100;
        tree.drawLine(x, y, myX, myY);
        if (n.left != null) drawTreeToSvg(n.left, myX, myY, l, myX);
        if (n.right != null) drawTreeToSvg(n.right, myX, myY, myX, r);
        tree.drawCircle(myX, myY, 40);
        tree.drawString(myX, myY, n.name);
    }

    public boolean parseFromFile(InputStreamReader file) {
        lexer = new SimpleLexer();

        ArrayList<TokenInfo> tokensInfo = new ArrayList<>();
        tokensInfo.add(new TokenInfo("IDENTIFIER", "[a-zA-Z_][a-zA-Z_0-9]*", null));
        tokensInfo.add(new TokenInfo("DELIMITER", "[.()]", null));
        tokensInfo.add(new TokenInfo("OPERATOR", ":-|,|;", null));
        lexer.setTokens(tokensInfo);

        lexer.setInput(file);

        try {
            current = lexer.nextToken();
            result = prolog();
            wasSuccessful = true;
            return true;
        } catch (SyntaxError ex) {
            wasSuccessful = false;
            errorMessage = ex.getMessage();
            errorWasSyntax = true;
            return false;
        } catch (SimpleLexer.UnrecognisedToken ex) {
            wasSuccessful = false;
            errorMessage = ex.getMessage();
            errorWasWithToken = true;
            return false;
        }
    }

    public void printLastTree() throws IOException {
        if (!wasSuccessful) {
            if (errorWasSyntax) {
                System.out.println("Syntax error:");
            } else if (errorWasWithToken) {
                System.out.println("Lexer error:");
            } else {
                System.out.println("Unknown error:");
            }
            System.out.println(errorMessage);
            return;
        }
        System.out.println("Code is correct.");
        System.out.println("Simple representation:");

        for (Node n : result) {
            System.out.println(n.toString());
        }
        int previousHeight = 0;
        int sumHeight = 0;
        int maxHeight = 0;
        for (Node n : result) {
            int x = getTreeHeight(n);
            sumHeight += x;
            maxHeight = Math.max(maxHeight, x);
        }
        int width = 200 * (int)Math.pow(2, maxHeight - 2);
        tree = new svgDraw(width, sumHeight * 100 + result.size() * 100, Color.WHITE);
        for (Node n : result) {
            int height = getTreeHeight(n);
            int w = 200 * (int)Math.pow(2, height - 2);
            drawTreeToSvg(n, width / 2, previousHeight, (width - w) / 2, (width + w) / 2);
            previousHeight += height * 100 + 100;
        }
        FileWriter f = new FileWriter("out.svg");
        f.write(tree.getSvgResult());
        f.close();
    }

    private String errorMessage = "";
    private boolean errorWasSyntax = false;
    private boolean errorWasWithToken = false;
    private ArrayList<Node> result;
    private boolean wasSuccessful = false;
    private svgDraw tree;
    private SimpleLexer lexer;
    private Token current;
}

