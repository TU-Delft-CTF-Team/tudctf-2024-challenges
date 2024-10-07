import java.util.*;

public class Challenge {
    public static void main(String[] args) {
        // Read a single line
        System.out.print("Enter the flag: ");
        String line = System.console().readLine();

        List<Character> encodedList = new ArrayList<>();
        for (char c : line.toCharArray()) {
            encodedList.add(c);
        }

        Random rand = new Random(1337);
        Collections.shuffle(encodedList, rand);

        StringBuilder encoded = new StringBuilder();
        for (char c : encodedList) {
            encoded.append(c);
        }

        if (encoded.toString().equals("113tkdl_Taf0lnu_1nsD3T4tc_sFs2dtggl_U_n_h{sC0}h_fs0n111")) {
            System.out.println("Correct flag!");
        } else {
            System.out.println("Incorrect flag!");
        }
    }
}