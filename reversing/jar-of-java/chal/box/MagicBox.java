package box;

import java.util.*;

public class MagicBox implements BaseBox {

    @Override
    public String doStuff(String inputString) {
        return Base64.getEncoder().encodeToString(inputString.getBytes());
    }
    
}
