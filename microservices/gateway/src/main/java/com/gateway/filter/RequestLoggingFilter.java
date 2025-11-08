package com.gateway.filter;

import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.context.RequestContext;
import com.netflix.zuul.exception.ZuulException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;
import java.util.Enumeration;

/**
 * Request Logging Filter
 * Logs incoming requests for monitoring and debugging
 */
@Component
public class RequestLoggingFilter extends ZuulFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(RequestLoggingFilter.class);
    
    @Override
    public String filterType() {
        return "pre";
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
        
        logger.info("Incoming request: {} {} from {}", 
            request.getMethod(), 
            request.getRequestURL(),
            request.getRemoteAddr());
        
        // Log headers
        Enumeration<String> headerNames = request.getHeaderNames();
        while (headerNames.hasMoreElements()) {
            String headerName = headerNames.nextElement();
            String headerValue = request.getHeader(headerName);
            logger.debug("Header: {} = {}", headerName, headerValue);
        }
        
        // Add request ID for tracing
        String requestId = java.util.UUID.randomUUID().toString();
        ctx.addZuulRequestHeader("X-Request-ID", requestId);
        logger.info("Request ID: {}", requestId);
        
        return null;
    }
}

