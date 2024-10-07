package box;

public class GarlicBox implements BaseBox {
    private final int r;

    public GarlicBox(int r) {
        this.r = r;
    }

    @Override
    public String doStuff(String inputString) {
        StringBuilder sb = new StringBuilder();
        for (char c : inputString.toCharArray()) {
            if (Character.isUpperCase(c)) {
                // Rotate the character by 3 positions
                sb.append((char) (((c - 'A' + r) % 26) + 'A'));
            } else if (Character.isLowerCase(c)) {
                // Rotate the character by 3 positions
                sb.append((char) (((c - 'a' + r) % 26) + 'a'));
            } else {
                sb.append(c);
            }
        }

        return sb.toString();
    }

}
