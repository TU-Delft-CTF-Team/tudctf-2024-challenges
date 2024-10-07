package fun.xitter.xitterbackend.services;

import fun.xitter.xitterbackend.dtos.UserLoginDTO;
import fun.xitter.xitterbackend.exceptions.UserAlreadyExistsException;
import fun.xitter.xitterbackend.models.User;
import fun.xitter.xitterbackend.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public User register(UserLoginDTO loginData) {
        if (userRepository.existsByUsername(loginData.username())) {
            throw new UserAlreadyExistsException("User with username " + loginData.username() + " already exists");
        }

        User user = new User();
        user.setUsername(loginData.username());
        user.setPassword(loginData.password());
        return userRepository.save(user);
    }

    public void followUser(User follower, User followed) {
        if (follower.getId().equals(followed.getId())) {
            throw new IllegalArgumentException("User cannot follow themselves");
        }
        follower.getFollowing().add(followed);
        userRepository.save(follower);
    }

    public void unfollowUser(User follower, User followed) {
        if (follower.getId().equals(followed.getId())) {
            throw new IllegalArgumentException("User cannot unfollow themselves");
        }
        follower.getFollowing().remove(followed);
        userRepository.save(follower);
    }
}
