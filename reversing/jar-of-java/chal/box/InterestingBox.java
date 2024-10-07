package box;

public class InterestingBox implements BaseBox {

    @Override
    public String doStuff(String inputString) {
        return new StringBuilder(inputString).reverse().toString();
    }
    
}
