package fun.xitter.xitterbackend.controllers;

import fun.xitter.xitterbackend.dtos.UserDTO;
import fun.xitter.xitterbackend.dtos.UserOverviewDTO;
import fun.xitter.xitterbackend.exceptions.ResourceNotFoundException;
import fun.xitter.xitterbackend.repositories.UserRepository;
import fun.xitter.xitterbackend.services.UserService;
import fun.xitter.xitterbackend.utils.UserManager;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/user")
public class UserController {
    private final UserManager userManager;
    private final UserRepository userRepository;
    private final UserService userService;

    @GetMapping("/me")
    public ResponseEntity<UserDTO> me(Authentication authentication) {
        return ResponseEntity.ok(new UserDTO(userManager.getUserFromAuthentication(authentication)));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(new UserDTO(userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"))));
    }

    @GetMapping("/overview/{id}")
    public ResponseEntity<UserOverviewDTO> getUserOverview(@PathVariable Long id) {
        return ResponseEntity.ok(new UserOverviewDTO(userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"))));
    }

    @PostMapping("/follow/{id}")
    public ResponseEntity<Void> followUser(@PathVariable Long id, Authentication authentication) {
        userService.followUser(userManager.getUserFromAuthentication(authentication), userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found")));
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/follow/{id}")
    public ResponseEntity<Void> unfollowUser(@PathVariable Long id, Authentication authentication) {
        userService.unfollowUser(userManager.getUserFromAuthentication(authentication), userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found")));
        return ResponseEntity.noContent().build();
    }
}
