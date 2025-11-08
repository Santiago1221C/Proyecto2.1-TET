#!/bin/bash
# Deployment script for Bookstore Microservices on Kubernetes

set -e

echo "=========================================="
echo "Deploying Bookstore Microservices"
echo "=========================================="

# Create namespace
echo "Creating namespace..."
kubectl apply -f namespace.yml

# Apply ConfigMaps and Secrets
echo "Applying ConfigMaps and Secrets..."
kubectl apply -f configmap.yml
kubectl apply -f secrets.yml

# Deploy databases
echo "Deploying databases..."
kubectl apply -f postgres-deployment.yml
kubectl apply -f mongodb-deployment.yml

# Wait for databases to be ready
echo "Waiting for databases to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n bookstore --timeout=300s
kubectl wait --for=condition=ready pod -l app=mongodb -n bookstore --timeout=300s

# Deploy RabbitMQ
echo "Deploying RabbitMQ..."
kubectl apply -f rabbitmq-deployment.yml

# Wait for RabbitMQ to be ready
echo "Waiting for RabbitMQ to be ready..."
kubectl wait --for=condition=ready pod -l app=rabbitmq -n bookstore --timeout=300s

# Deploy microservices
echo "Deploying microservices..."
kubectl apply -f user-deployment.yml
kubectl apply -f payment-deployment.yml
kubectl apply -f review-deployment.yml

# Wait for services to be ready
echo "Waiting for services to be ready..."
kubectl wait --for=condition=ready pod -l app=user-service -n bookstore --timeout=300s
kubectl wait --for=condition=ready pod -l app=payment-service -n bookstore --timeout=300s
kubectl wait --for=condition=ready pod -l app=review-service -n bookstore --timeout=300s

# Deploy frontend
echo "Deploying frontend..."
kubectl apply -f frontend-deployment.yml

# Wait for frontend to be ready
echo "Waiting for frontend to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend -n bookstore --timeout=300s

# Apply ingress
echo "Applying ingress..."
kubectl apply -f ingress.yml

echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="

# Get service information
echo ""
echo "Service Status:"
kubectl get pods -n bookstore
echo ""
kubectl get services -n bookstore
echo ""
echo "To access the application, get the LoadBalancer URL:"
echo "kubectl get ingress -n bookstore"



