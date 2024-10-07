package fun.xitter.xitterbackend.models;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;

@Entity
@Getter
@Setter
public class Post {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    private Long id;

    @Size(max = 255)
    @NotEmpty
    @Column(nullable = false)
    private String content;

    @Column(nullable = false)
    @CreationTimestamp
    private java.sql.Timestamp createdAt;

    @Column(nullable = false)
    private boolean isDeleted = false;

    @Column(nullable = false)
    private boolean isPrivate = false;

    @ManyToOne(cascade = CascadeType.ALL, optional = false)
    @JoinColumn(name = "author_id", nullable = false)
    @JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
    private User author;
}
