package box;

public class AmazingBox implements BaseBox {

    @Override
    public String doStuff(String inputString) {
        return inputString.substring(0, 5) + "Amazing" + inputString.length() + inputString.substring(5);
    }
    
}
