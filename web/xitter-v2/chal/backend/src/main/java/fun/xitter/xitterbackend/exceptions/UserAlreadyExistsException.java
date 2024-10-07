package fun.xitter.xitterbackend.exceptions;

public class UserAlreadyExistsException extends IllegalStateException {
    public UserAlreadyExistsException(String message) {
        super(message);
    }

    public UserAlreadyExistsException() {
        this("User already exists");
    }
}
