package fun.xitter.xitterbackend.services;

import fun.xitter.xitterbackend.dtos.PostCreateDTO;
import fun.xitter.xitterbackend.models.Post;
import fun.xitter.xitterbackend.models.User;
import fun.xitter.xitterbackend.repositories.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class PostService {
    private final PostRepository postRepository;

    public Post createPost(PostCreateDTO postDTO, User author) {
        Post post = new Post();
        post.setContent(postDTO.content());
        post.setPrivate(postDTO.isPrivate());
        post.setAuthor(author);

        return postRepository.save(post);
    }
}
