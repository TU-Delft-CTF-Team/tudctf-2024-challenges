package fun.xitter.xitterbackend.utils;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Date;

@Component
public class JWTHandler {
    @Value("${jwt.secret}")
    private String secret;

    public String generateToken(String username) {
        return JWT.create()
                .withSubject("User")
                .withClaim("username", username)
                .withIssuedAt(new Date())
                .sign(Algorithm.HMAC256(secret));
    }

    public String validateToken(String token) {
        DecodedJWT jwt = JWT.require(Algorithm.HMAC256(secret))
                .withSubject("User")
                .build()
                .verify(token);

        return jwt.getClaim("username").asString();
    }
}
