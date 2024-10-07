package fun.xitter.xitterbackend.dtos;

import fun.xitter.xitterbackend.models.User;
import fun.xitter.xitterbackend.models.UserRole;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.io.Serializable;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * DTO for {@link fun.xitter.xitterbackend.models.User}
 */
public record UserDTO(Long id, @Size(min = 3, max = 32) @Pattern(regexp = "[a-z0-9-_]+") @NotBlank String username,
                      @NotBlank String password, boolean isBanned, UserRole role, Set<UserDto> following,
                      Set<UserDto> followers) implements Serializable {
    /**
     * DTO for {@link fun.xitter.xitterbackend.models.User}
     */
    public record UserDto(Long id, String username) implements Serializable {
    }

    public UserDTO(User user) {
        this(user.getId(), user.getUsername(), user.getPassword(), user.isBanned(), user.getRole(),
                user.getFollowing().stream().map(u -> new UserDto(u.getId(), u.getUsername())).collect(Collectors.toSet()),
                user.getFollowers().stream().map(u -> new UserDto(u.getId(), u.getUsername())).collect(Collectors.toSet()));
    }
}