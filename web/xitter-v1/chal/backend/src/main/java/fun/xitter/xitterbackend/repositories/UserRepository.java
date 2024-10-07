package fun.xitter.xitterbackend.repositories;

import fun.xitter.xitterbackend.models.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.lang.NonNull;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(@NonNull String username);

    boolean existsByUsername(String username);
}