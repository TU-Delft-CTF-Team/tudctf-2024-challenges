package box;

import java.util.*;

public class MainClass {
    public static void main(String[] args) {
        System.out.print("Enter the flag: ");
        String input = System.console().readLine();

        List<BaseBox> boxes = List.of(new GarlicBox(5), new AmazingBox(), new MagicBox(), new InterestingBox(),
                new PersianBox());

        for (BaseBox box : boxes) {
            input = box.doStuff(input);
        }

        if (input.equals(
                "nahp2XzgmbPersian9Nzdz0mYkdX1yZyRTcfNXMfl2MwRDM41CbzFzczFTd49VazRzXsNXMzNXM1h3eLBjNn5Wa6FWbBlFSJpVW")) {
            System.out.println("Correct flag!");
        } else {
            System.out.println("Incorrect flag!");
        }
    }
}