package fun.xitter.xitterbackend.controllers;

import fun.xitter.xitterbackend.dtos.TokenDTO;
import fun.xitter.xitterbackend.dtos.UserLoginDTO;
import fun.xitter.xitterbackend.models.User;
import fun.xitter.xitterbackend.services.UserService;
import fun.xitter.xitterbackend.utils.JWTHandler;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.net.URI;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final UserService userService;
    private final AuthenticationManager authenticationManager;
    private final JWTHandler jwtHandler;

    @PostMapping("/login")
    public ResponseEntity<TokenDTO> login(@Valid @RequestBody UserLoginDTO loginData) {
        UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(loginData.username(),
                loginData.password());

        Authentication authentication = authenticationManager.authenticate(authToken);
        SecurityContextHolder.getContext().setAuthentication(authentication);

        return ResponseEntity.ok(new TokenDTO(jwtHandler.generateToken(loginData.username())));
    }

    @PostMapping("/register")
    public ResponseEntity<Void> register(@Valid @RequestBody UserLoginDTO registrationData) {
        User user = userService.register(registrationData);
        return ResponseEntity.created(URI.create("/api/user/" + user.getId())).build();
    }
}
