package fun.xitter.xitterbackend.repositories;

import fun.xitter.xitterbackend.models.Post;
import fun.xitter.xitterbackend.models.User;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface PostRepository extends JpaRepository<Post, Long> {
  @Query("SELECT p FROM Post p WHERE (p.isPrivate = false OR p.author.id = :#{#user.id}) " +
          "AND p.isDeleted = false ORDER BY p.createdAt DESC")
  List<Post> getLatestPosts(Pageable pageable, @Param("user") User user);

  @Query("SELECT p FROM Post p WHERE p.author.id = :id AND p.isDeleted = false ORDER BY p.createdAt DESC")
  List<Post> findByAuthorId(Long id);

  @Query("SELECT p FROM Post p WHERE (p.author.id = :#{#currentUser.id} OR p.isPrivate = false) " +
          "AND p.isDeleted = false AND p.author.id = :id ORDER BY p.createdAt DESC")
  List<Post> findByAuthorId(Long id, @Param("currentUser") User currentUser);

  @Query("SELECT p FROM Post p WHERE p.id = :id AND (p.author.id = :#{#currentUser.id} OR p.isPrivate = false) " +
          "AND p.isDeleted = false")
  Optional<Post> findByIdAndCurrentUser(Long id, User currentUser);
}