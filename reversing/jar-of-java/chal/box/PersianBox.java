package box;

public class PersianBox implements BaseBox {

    @Override
    public String doStuff(String inputString) {
        return inputString.substring(10, 20) + "Persian" + inputString.substring(0, 10) + inputString.substring(20);
    }

}
