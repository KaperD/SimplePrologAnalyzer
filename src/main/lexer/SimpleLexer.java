package lexer;

import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.function.Consumer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class SimpleLexer {

    public static class UnrecognisedToken extends RuntimeException {
        UnrecognisedToken() {}
        UnrecognisedToken(String errorMessage) {
            super(errorMessage);
        }
    }

    /**
     * Sets {@code SimpleLexer} input.
     *
     * @param text A string to analyze.
     */
    public void setInput(String text) {
        scan = new Scanner(new String(text));
    }

    /**
     * Reads a text from file reader ans sets to {@code SimpleLexer} input.
     *
     * @param fileReader A file reader to analyze.
     */
    public void setInput(InputStreamReader fileReader) {
        StringBuilder newText = new StringBuilder();
        Scanner fileScan = new Scanner(fileReader);
        while (fileScan.hasNextLine()) {
            newText.append(fileScan.nextLine()).append("\n");
        }
        setInput(newText.toString());
    }

    /**
     * Sets reserved words list to {@code SimpleLexer}.
     * They have biggest priority.
     *
     * @param reserved {@code ArrayList} of {@code TokenInfo} about reserved words.
     */
    public void setReserved(ArrayList<TokenInfo> reserved) {
        this.reserved = new ArrayList<>(reserved);
    }

    /**
     * Sets tokens list to {@code SimpleLexer}.
     * Their priority equals to their order in {@code ArrayList}
     *
     * @param tokens {@code ArrayList} of {@code TokenInfo} about tokens.
     */
    public void setTokens(ArrayList<TokenInfo> tokens) {
        this.tokens = new ArrayList<>(tokens);
    }

    /**
     * Sets words, which are ignored
     *
     * @param wordsToIgnore {@code String[]} of words to ignore.
     */
    public void setIgnore(String[] wordsToIgnore) {
        StringBuilder newIgnore = new StringBuilder();
        for (String s : wordsToIgnore) {
            newIgnore.append(s).append("+|");
        }
        newIgnore.append("\\p{javaWhitespace}+");
        ignore = Pattern.compile(newIgnore.toString());
    }

    /**
     * Tries to find next token
     *
     * @return next token
     *
     * @throws UnrecognisedToken if hasn't recognised word
     */
    public Token nextToken() {
        if (firstToken) {
            firstToken = false;
            if (ignore == null) {
                ignore = Pattern.compile("\\p{javaWhitespace}+");
            }
            ArrayList<TokenInfo> all = new ArrayList<>();
            if (reserved != null) all.addAll(reserved);
            if (tokens != null) all.addAll(tokens);
            tokens = all;
            reserved = null;
        }
        while (true) {
            Matcher matcher = ignore.matcher(lastToken);
            while (matcher.find() && matcher.start() == 0) {
                positionInLine += matcher.group().length();
                lastToken = lastToken.replaceFirst(ignore.pattern(), "");
                matcher = ignore.matcher(lastToken);
            }
            if (!scan.hasNextLine() && lastToken.isEmpty()) return null;
            if (lastToken.isEmpty()) {
                lastToken = scan.nextLine();
                currentLine = lastToken;
                ++lineNumber;
                positionInLine = 0;
            } else {
                break;
            }
        }
        for (TokenInfo info : tokens) {
            String tokenName = info.name;
            String regex = info.regex;
            Pattern pattern = Pattern.compile(regex);
            Matcher matcher = pattern.matcher(lastToken);
            if (matcher.find() && matcher.start() == 0) {
                Token ret = new Token(tokenName, matcher.group(), lineNumber, positionInLine);
                positionInLine += matcher.group().length();
                lastToken = lastToken.replaceFirst(regex, "");
                Consumer<Token> consumer = info.func;
                if (consumer != null) {
                    consumer.accept(ret);
                }
                return ret;
            }
        }
        throw new UnrecognisedToken(String.format("Line %d column %d: Unrecognised token: '%s'",
                lineNumber, positionInLine, lastToken));
    }

    /**
     *
     * @return current line of text
     */
    public String getCurrentLine() {
        return currentLine;
    }

    /**
     *
     * @return current line number
     */
    public int getLineNumber() {
        return lineNumber;
    }

    private int lineNumber = 0;
    private int positionInLine = 0;

    private ArrayList<TokenInfo> reserved;
    private ArrayList<TokenInfo> tokens;

    private String lastToken = "";
    private String currentLine = "";
    private Scanner scan;

    private Pattern ignore;

    private boolean firstToken = true;
}

