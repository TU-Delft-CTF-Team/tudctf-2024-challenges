package fun.xitter.xitterbackend.utils;

import fun.xitter.xitterbackend.models.User;
import fun.xitter.xitterbackend.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class UserManager {
    private final UserRepository userRepository;

    public User getUserFromAuthentication(Authentication auth) {
        return userRepository.findByUsername(auth.getName())
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }
}
