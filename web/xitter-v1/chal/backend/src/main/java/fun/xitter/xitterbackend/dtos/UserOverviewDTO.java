package fun.xitter.xitterbackend.dtos;

import fun.xitter.xitterbackend.models.User;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.io.Serializable;

/**
 * DTO for {@link fun.xitter.xitterbackend.models.User}
 */
public record UserOverviewDTO(
        Long id,
        @Size(min = 3, max = 32) @Pattern(regexp = "[a-z0-9-_]+") @NotBlank String username,
        int followers,
        int following,
        int posts
) implements Serializable {
  public UserOverviewDTO(User user) {
    this(user.getId(),
            user.getUsername(),
            user.getFollowers().size(),
            user.getFollowing().size(),
            user.getPosts().size());
  }
}