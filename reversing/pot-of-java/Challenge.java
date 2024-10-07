// flag TUDCTF{i_th0ught_this_w4s_t3a}
public class Challenge {
    public static void incorrect() {
        System.out.println("Sorry, that is not the correct flag. Please try again.");
        System.exit(1);
    }

    public static void main(String[] args) {
        System.out.print("Please enter the flag: ");
        String flag = System.console().readLine();

        if (flag.length() != 30) {
            incorrect();
        }

        if (flag.charAt(0) != 'T') {
            incorrect();
        }

        if (flag.charAt(1) != 'U') {
            incorrect();
        }

        if (flag.charAt(2) != 'D') {
            incorrect();
        }

        if (flag.charAt(3) != 'C') {
            incorrect();
        }

        if (flag.charAt(4) != 'T') {
            incorrect();
        }

        if (flag.charAt(5) != 'F') {
            incorrect();
        }

        if (flag.charAt(6) != '{') {
            incorrect();
        }

        if (flag.charAt(7) != 'i') {
            incorrect();
        }

        if (flag.charAt(8) != '_') {
            incorrect();
        }

        if (flag.charAt(9) != 't') {
            incorrect();
        }

        if (flag.charAt(10) != 'h') {
            incorrect();
        }

        if (flag.charAt(11) != '0') {
            incorrect();
        }

        if (flag.charAt(12) != 'u') {
            incorrect();
        }

        if (flag.charAt(13) != 'g') {
            incorrect();
        }

        if (flag.charAt(14) != 'h') {
            incorrect();
        }

        if (flag.charAt(15) != 't') {
            incorrect();
        }

        if (flag.charAt(16) != '_') {
            incorrect();
        }

        if (flag.charAt(17) != 't') {
            incorrect();
        }

        if (flag.charAt(18) != 'h') {
            incorrect();
        }

        if (flag.charAt(19) != 'i') {
            incorrect();
        }

        if (flag.charAt(20) != 's') {
            incorrect();
        }

        if (flag.charAt(21) != '_') {
            incorrect();
        }

        if (flag.charAt(22) != 'w') {
            incorrect();
        }

        if (flag.charAt(23) != '4') {
            incorrect();
        }

        if (flag.charAt(24) != 's') {
            incorrect();
        }

        if (flag.charAt(25) != '_') {
            incorrect();
        }

        if (flag.charAt(26) != 't') {
            incorrect();
        }

        if (flag.charAt(27) != '3') {
            incorrect();
        }

        if (flag.charAt(28) != 'a') {
            incorrect();
        }

        if (flag.charAt(29) != '}') {
            incorrect();
        }

        System.out.println("Congratulations! You have successfully completed the challenge.");
    }
}
