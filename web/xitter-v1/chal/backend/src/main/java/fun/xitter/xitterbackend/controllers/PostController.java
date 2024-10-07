package fun.xitter.xitterbackend.controllers;

import fun.xitter.xitterbackend.dtos.PostCreateDTO;
import fun.xitter.xitterbackend.dtos.PostDTO;
import fun.xitter.xitterbackend.exceptions.ResourceNotFoundException;
import fun.xitter.xitterbackend.repositories.PostRepository;
import fun.xitter.xitterbackend.services.PostService;
import fun.xitter.xitterbackend.utils.UserManager;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/post")
public class PostController {
    private final PostRepository postRepository;
    private final PostService postService;
    private final UserManager userManager;

    @GetMapping("/{id}")
    public ResponseEntity<PostDTO> getPost(@PathVariable Long id, Authentication authentication) {
        return ResponseEntity.ok(new PostDTO(
                postRepository.findByIdAndCurrentUser(id, userManager.getUserFromAuthentication(authentication))
                        .orElseThrow(() -> new ResourceNotFoundException("Post not found"))));
    }

    @PostMapping("/create")
    public ResponseEntity<PostDTO> createPost(@RequestBody @Validated PostCreateDTO post, Authentication authentication) {
        return ResponseEntity.ok(
                new PostDTO(postService.createPost(post, userManager.getUserFromAuthentication(authentication))));
    }

    @GetMapping("/latest")
    public ResponseEntity<List<PostDTO>> getLatestPosts(@RequestParam(value = "page", defaultValue = "0") int page,
                                                        @RequestParam(value = "size", defaultValue = "25") int size,
                                                        Authentication authentication) {
        Pageable pageRequest = PageRequest.of(page, size);
        return ResponseEntity.ok(postRepository.getLatestPosts(pageRequest,
                userManager.getUserFromAuthentication(authentication)).stream().map(PostDTO::new).toList());
    }

    @GetMapping("/user/{id}")
    public ResponseEntity<List<PostDTO>> getPostsByUser(@PathVariable Long id) {
        return ResponseEntity.ok(postRepository.findByAuthorId(id).stream().map(PostDTO::new).toList());
    }
}
