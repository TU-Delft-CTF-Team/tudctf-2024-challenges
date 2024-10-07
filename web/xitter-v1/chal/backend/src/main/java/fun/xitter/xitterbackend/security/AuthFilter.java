package fun.xitter.xitterbackend.security;

import com.auth0.jwt.exceptions.JWTDecodeException;
import com.auth0.jwt.exceptions.SignatureVerificationException;
import com.auth0.jwt.exceptions.TokenExpiredException;
import fun.xitter.xitterbackend.utils.JWTHandler;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.NoSuchElementException;

@Component
@RequiredArgsConstructor
public class AuthFilter extends OncePerRequestFilter {
    private final JWTHandler jwtHandler;
    private final CustomUserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        String authHeader = request.getHeader("Authorization");

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String jwt = authHeader.substring(7);
            if (!jwt.isBlank()) {
                try {
                    String username = jwtHandler.validateToken(jwt);
                    UserDetails authDAO = userDetailsService.loadUserByUsername(username);
                    UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(username,
                            authDAO.getPassword(),
                            authDAO.getAuthorities());

                    if (SecurityContextHolder.getContext().getAuthentication() == null) {
                        SecurityContextHolder.getContext().setAuthentication(authToken);
                    }
                } catch (TokenExpiredException exc) {
                    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "JWT Token has expired");
                } catch (SignatureVerificationException ex) {
                    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid JWT Token");
                } catch (NoSuchElementException | UsernameNotFoundException ex) {
                    response.sendError(HttpServletResponse.SC_CONFLICT, "JWT Token's user no longer exists");
                } catch (JWTDecodeException ex) {
                    response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Malformed request");
                }
            }
        }

        filterChain.doFilter(request, response);
    }
}
