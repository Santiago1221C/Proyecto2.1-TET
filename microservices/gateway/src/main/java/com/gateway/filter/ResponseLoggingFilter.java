package com.gateway.filter;

import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.context.RequestContext;
import com.netflix.zuul.exception.ZuulException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Response Logging Filter
 * Logs outgoing responses for monitoring and debugging
 */
@Component
public class ResponseLoggingFilter extends ZuulFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(ResponseLoggingFilter.class);
    
    @Override
    public String filterType() {
        return "post";
    }
    
    @Override
    public int filterOrder() {
        return 1;
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
        
        String requestId = ctx.getZuulRequestHeaders().get("X-Request-ID");
        
        logger.info("Outgoing response: {} {} - Status: {} - Request ID: {}", 
            request.getMethod(), 
            request.getRequestURL(),
            response.getStatus(),
            requestId);
        
        // Add response headers
        response.setHeader("X-Request-ID", requestId);
        response.setHeader("X-Gateway-Service", "bookstore-gateway");
        
        return null;
    }
}

