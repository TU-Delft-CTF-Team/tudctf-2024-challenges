package fun.xitter.xitterbackend.dtos;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@EqualsAndHashCode
@ToString
@Builder
public class APIError {
    @Builder.Default
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd-MM-yyyy HH:mm:ss")
    private LocalDateTime timestamp = LocalDateTime.now();

    private int status;

    private String description;

    @Builder.Default
    private List<String> errors = new ArrayList<>();

    public void addError(String error) {
        errors.add(error);
    }
}
