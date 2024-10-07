package fun.xitter.xitterbackend.dtos;

import fun.xitter.xitterbackend.models.User;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.io.Serializable;

/**
 * DTO for {@link User}
 */
public record UserLoginDTO(@Size(min = 3, max = 32) @Pattern(regexp = "[a-z0-9-_]+") @NotBlank String username,
                           @Size(min = 8, max = 64) @NotBlank String password) implements Serializable {
}