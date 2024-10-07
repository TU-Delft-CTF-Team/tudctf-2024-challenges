package fun.xitter.xitterbackend.dtos;

import fun.xitter.xitterbackend.models.Post;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.io.Serializable;

/**
 * DTO for {@link Post}
 */
public record PostCreateDTO(@Size(max = 255) @NotEmpty String content, boolean isPrivate) implements Serializable {
}