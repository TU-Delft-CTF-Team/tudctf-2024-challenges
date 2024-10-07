package fun.xitter.xitterbackend.dtos;

import fun.xitter.xitterbackend.models.Post;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import java.io.Serializable;
import java.sql.Timestamp;

/**
 * DTO for {@link fun.xitter.xitterbackend.models.Post}
 */
public record PostDTO(Long id, @Size(max = 255) @NotEmpty String content, Timestamp createdAt, boolean isDeleted,
                      boolean isPrivate, Long authorId, String authorUsername) implements Serializable {

    public PostDTO(Post post) {
        this(post.getId(), post.getContent(), post.getCreatedAt(), post.isDeleted(), post.isPrivate(),
                post.getAuthor().getId(), post.getAuthor().getUsername());
    }
}