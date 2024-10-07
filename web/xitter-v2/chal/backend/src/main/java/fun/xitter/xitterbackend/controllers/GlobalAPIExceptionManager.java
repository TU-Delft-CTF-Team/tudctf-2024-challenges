package fun.xitter.xitterbackend.controllers;

import fun.xitter.xitterbackend.dtos.APIError;
import fun.xitter.xitterbackend.exceptions.ResourceNotFoundException;
import fun.xitter.xitterbackend.exceptions.UserAlreadyExistsException;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.util.List;

@ControllerAdvice
@Order(Ordered.HIGHEST_PRECEDENCE)
public class GlobalAPIExceptionManager {
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ResponseBody
    @ExceptionHandler(IllegalArgumentException.class)
    public APIError handleIllegalArgumentException(IllegalArgumentException ex) {
        return APIError.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .description(ex.getMessage())
                .build();
    }

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ResponseBody
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public APIError handleValidationException(MethodArgumentNotValidException ex) {
        BindingResult result = ex.getBindingResult();

        List<FieldError> fieldErrors = result.getFieldErrors();

        APIError apiError = APIError.builder()
                .status(HttpStatus.BAD_REQUEST.value())
                .build();
        for (FieldError fieldError : fieldErrors) {
            apiError.addError(fieldError.getDefaultMessage());
        }

        return apiError;
    }

    @ResponseStatus(HttpStatus.CONFLICT)
    @ResponseBody
    @ExceptionHandler({UserAlreadyExistsException.class})
    public APIError handleConflictException(Exception ex) {
        return APIError.builder()
                .status(HttpStatus.CONFLICT.value())
                .description(ex.getMessage())
                .build();
    }

    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ResponseBody
    @ExceptionHandler({ResourceNotFoundException.class})
    public APIError handleNotFoundException(Exception ex) {
        return APIError.builder()
                .status(HttpStatus.NOT_FOUND.value())
                .description(ex.getMessage())
                .build();
    }

    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    @ResponseBody
    @ExceptionHandler({AccessDeniedException.class})
    public APIError handleUnauthorizedException(Exception ex) {
        return APIError.builder()
                .status(HttpStatus.UNAUTHORIZED.value())
                .description(ex.getMessage())
                .build();
    }
}
