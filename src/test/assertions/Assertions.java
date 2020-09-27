package assertions;

import java.util.ArrayList;

public class Assertions {
    public static void assertTrue(boolean state, int testNumber) {
        if (!state) {
            ++incorrect;
            fails.add(String.format("Test number %d failed in test group %s", testNumber, Thread.currentThread().getStackTrace()[2].getMethodName()));
        } else {
            ++correct;
        }
    }

    public static void assertFalse(boolean state, int testNumber) {
        if (state) {
            ++incorrect;
            fails.add(String.format("Test number %d failed in test group %s", testNumber, Thread.currentThread().getStackTrace()[2].getMethodName()));
        } else {
            ++correct;
        }
    }

    public static void printResult() {
        System.out.printf("Passed: %d, Failed: %d%n", correct, incorrect);
        for (String s : fails) {
            System.out.println(s);
        }
    }

    static int correct = 0;
    static int incorrect = 0;
    static ArrayList<String> fails = new ArrayList<>();
}