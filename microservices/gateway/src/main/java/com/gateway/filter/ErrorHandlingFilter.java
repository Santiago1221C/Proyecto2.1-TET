package com.gateway.filter;

import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.context.RequestContext;
import com.netflix.zuul.exception.ZuulException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Error Handling Filter
 * Handles errors and provides standardized error responses
 */
@Component
public class ErrorHandlingFilter extends ZuulFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(ErrorHandlingFilter.class);
    
    @Override
    public String filterType() {
        return "error";
    }
    
    @Override
    public int filterOrder() {
        return 0;
    }
    
    @Override
    public boolean shouldFilter() {
        return true;
    }
    
    @Override
    public Object run() throws ZuulException {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();
        HttpServletResponse response = ctx.getResponse();
        
        Throwable throwable = ctx.getThrowable();
        String requestId = ctx.getZuulRequestHeaders().get("X-Request-ID");
        
        logger.error("Error processing request: {} {} - Request ID: {} - Error: {}", 
            request.getMethod(), 
            request.getRequestURL(),
            requestId,
            throwable != null ? throwable.getMessage() : "Unknown error");
        
        // Set error response
        response.setStatus(HttpStatus.INTERNAL_SERVER_ERROR.value());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        
        // Create error response
        Map<String, Object> errorResponse = new HashMap<>();
        errorResponse.put("status", "error");
        errorResponse.put("message", "Internal server error");
        errorResponse.put("requestId", requestId);
        errorResponse.put("timestamp", java.time.LocalDateTime.now().toString());
        
        if (throwable != null) {
            errorResponse.put("error", throwable.getMessage());
        }
        
        // Write error response
        try {
            response.getWriter().write(convertToJson(errorResponse));
        } catch (IOException e) {
            logger.error("Failed to write error response: {}", e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Convert object to JSON string
     * 
     * @param obj Object to convert
     * @return JSON string
     */
    private String convertToJson(Object obj) {
        try {
            com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
            return mapper.writeValueAsString(obj);
        } catch (Exception e) {
            logger.error("Failed to convert object to JSON: {}", e.getMessage());
            return "{\"status\":\"error\",\"message\":\"Internal server error\"}";
        }
    }
}

