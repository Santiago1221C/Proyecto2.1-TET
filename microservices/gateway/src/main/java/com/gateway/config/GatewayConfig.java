package com.gateway.config;

import org.springframework.cloud.netflix.zuul.filters.ZuulProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import springfox.documentation.swagger.web.SwaggerResource;
import springfox.documentation.swagger.web.SwaggerResourcesProvider;

import java.util.ArrayList;
import java.util.List;

/**
 * Gateway Configuration
 * Configuration for API Gateway routing and Swagger documentation
 */
@Configuration
public class GatewayConfig {
    
    /**
     * Zuul properties configuration
     * 
     * @return ZuulProperties bean
     */
    @Bean
    @Primary
    public ZuulProperties zuulProperties() {
        return new ZuulProperties();
    }
    
    /**
     * Swagger resources provider for API documentation
     * 
     * @return SwaggerResourcesProvider bean
     */
    @Bean
    public SwaggerResourcesProvider swaggerResourcesProvider() {
        return new SwaggerResourcesProvider() {
            @Override
            public List<SwaggerResource> get() {
                List<SwaggerResource> resources = new ArrayList<>();
                
                // User Service
                resources.add(createSwaggerResource("user-service", "/user-service/v2/api-docs", "2.0"));
                
                // Payment Service (Python)
                resources.add(createSwaggerResource("payment-service-python", "/payment-service-python/api-docs", "2.0"));
                
                // Payment Service (Java)
                resources.add(createSwaggerResource("payment-service-java", "/payment-service-java/v2/api-docs", "2.0"));
                
                // Review Service
                resources.add(createSwaggerResource("review-service", "/review-service/v2/api-docs", "2.0"));
                
                return resources;
            }
        };
    }
    
    /**
     * Create Swagger resource
     * 
     * @param name Resource name
     * @param location Resource location
     * @param version API version
     * @return SwaggerResource
     */
    private SwaggerResource createSwaggerResource(String name, String location, String version) {
        SwaggerResource swaggerResource = new SwaggerResource();
        swaggerResource.setName(name);
        swaggerResource.setLocation(location);
        swaggerResource.setSwaggerVersion(version);
        return swaggerResource;
    }
}

