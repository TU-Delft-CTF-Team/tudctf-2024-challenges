public class Challenge {
    public static void main(String[] args) {
        System.out.print("Please enter the flag: ");
        String flag = System.console().readLine();

        if (flag.equals("TUDCTF{jav4_is_fun_and_3a5y_to_revers3}")) {
            System.out.println("Congratulations! You have successfully completed the challenge.");
        } else {
            System.out.println("Sorry, that is not the correct flag. Please try again.");
        }
    }
}