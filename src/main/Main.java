import java.io.*;

import parser.Parser;


public class Main {
    public static void main(String[] args) throws IOException {
        Parser p = new Parser();
        InputStreamReader file = null;
        if (args.length == 1) {
             file = new FileReader(args[0]);
        } else if (args.length == 2 && (args[0].equals("-s") || args[0].equals("--string"))) {
            file = new InputStreamReader(new ByteArrayInputStream(args[1].getBytes()));
        } else {
            System.out.println("Wrong arguments");
            System.exit(1);
        }
        p.parseFromFile(file);
        p.printLastTree();
        file.close();
    }
}
