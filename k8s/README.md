# Bookstore Microservices - Kubernetes Deployment

Este proyecto implementa una arquitectura de microservicios para una librería online con las siguientes características:

## Arquitectura

### Microservicios
- **Gateway Service** (Java): API Gateway con Zuul para enrutamiento y balanceo de carga
- **User Service** (Java): Gestión de usuarios y autenticación
- **Payment Service Python** (Python): Procesamiento de pagos con Flask
- **Payment Service Java** (Java): Procesamiento de pagos con Spring Boot
- **Review Service** (Python): Gestión de reseñas de libros

### Bases de Datos
- **PostgreSQL**: Base de datos principal (StatefulSet)
- **MongoDB**: Base de datos para documentos (StatefulSet)

### Message Broker
- **RabbitMQ**: Comunicación asíncrona entre microservicios (StatefulSet)

### Monitoreo y Logging
- **Prometheus**: Métricas y alertas
- **Grafana**: Dashboards de monitoreo
- **Elasticsearch**: Almacenamiento de logs
- **Kibana**: Visualización de logs
- **Filebeat**: Recolección de logs

## Características Implementadas

### ✅ Requisitos del Proyecto
- [x] **Mínimo 2 lenguajes**: Python y Java
- [x] **Comunicación asíncrona**: RabbitMQ entre microservicios
- [x] **Comunicación síncrona**: REST API a través del Gateway
- [x] **Mínimo 2 réplicas**: Todos los microservicios configurados con 2+ réplicas
- [x] **Kubernetes**: Despliegue completo con StatefulSets para persistencia
- [x] **Escalabilidad**: HPA (Horizontal Pod Autoscaler) configurado
- [x] **Alta disponibilidad**: Anti-afinidad de pods y tolerancias

### ✅ Buenas Prácticas Implementadas

#### 1. Validación y Manejo de Errores
- Validación robusta de datos de entrada
- Manejo centralizado de errores
- Respuestas API estandarizadas
- Logging estructurado

#### 2. Comunicación
- **Síncrona**: REST API con API Gateway
- **Asíncrona**: RabbitMQ con retry y circuit breakers
- **Circuit Breakers**: Para tolerancia a fallos
- **Retry Policies**: Con backoff exponencial

#### 3. Persistencia
- **StatefulSets** para bases de datos
- **PersistentVolumeClaims** para almacenamiento
- **ConfigMaps** para configuración
- **Secrets** para datos sensibles

#### 4. Monitoreo y Observabilidad
- **Métricas**: Prometheus con alertas
- **Dashboards**: Grafana con visualizaciones
- **Logs**: Elasticsearch + Kibana
- **Health Checks**: Liveness, readiness y startup probes

#### 5. Seguridad
- **Secrets** para credenciales
- **Network Policies** (configurables)
- **RBAC** (configurables)
- **Validación de entrada** en todos los endpoints

#### 6. Escalabilidad
- **HPA** configurado para todos los servicios
- **Anti-afinidad** de pods para distribución
- **Resource limits** y requests
- **Circuit breakers** para prevenir cascadas de fallos

## Estructura de Archivos

```
k8s/
├── namespace.yml                    # Namespace del proyecto
├── configmap.yml                   # Configuración de la aplicación
├── secrets.yml                     # Secretos (crear manualmente)
├── gateway-deployment.yml          # API Gateway
├── user-deployment.yml             # Servicio de usuarios
├── payment-deployment.yml          # Servicio de pagos Python
├── payment-java-deployment.yml     # Servicio de pagos Java
├── review-deployment.yml           # Servicio de reseñas
├── postgres-statefulset.yml        # PostgreSQL StatefulSet
├── mongodb-statefulset.yml         # MongoDB StatefulSet
├── rabbitmq-statefulset.yml        # RabbitMQ StatefulSet
├── ingress.yml                     # Ingress para acceso externo
└── monitoring/
    ├── prometheus-deployment.yml   # Prometheus
    ├── grafana-deployment.yml      # Grafana
    └── elasticsearch-deployment.yml # Elasticsearch + Kibana + Filebeat
```

## Despliegue

### 1. Crear Namespace
```bash
kubectl apply -f namespace.yml
```

### 2. Crear Secrets
```bash
# Crear archivo secrets.yml con los valores reales
kubectl apply -f secrets.yml
```

### 3. Aplicar ConfigMaps
```bash
kubectl apply -f configmap.yml
```

### 4. Desplegar Bases de Datos
```bash
kubectl apply -f postgres-statefulset.yml
kubectl apply -f mongodb-statefulset.yml
kubectl apply -f rabbitmq-statefulset.yml
```

### 5. Desplegar Microservicios
```bash
kubectl apply -f user-deployment.yml
kubectl apply -f payment-deployment.yml
kubectl apply -f payment-java-deployment.yml
kubectl apply -f review-deployment.yml
kubectl apply -f gateway-deployment.yml
```

### 6. Desplegar Monitoreo
```bash
kubectl apply -f monitoring/prometheus-deployment.yml
kubectl apply -f monitoring/grafana-deployment.yml
kubectl apply -f monitoring/elasticsearch-deployment.yml
```

### 7. Configurar Ingress
```bash
kubectl apply -f ingress.yml
```

## Acceso a Servicios

### API Gateway
```bash
# Obtener IP del LoadBalancer
kubectl get service gateway-service -n bookstore

# Acceder a la API
curl http://<GATEWAY_IP>/api/users/health
curl http://<GATEWAY_IP>/api/payments-python/health
curl http://<GATEWAY_IP>/api/payments-java/actuator/health
```

### Monitoreo
```bash
# Prometheus
kubectl port-forward service/prometheus-service 9090:9090 -n bookstore

# Grafana
kubectl port-forward service/grafana-service 3000:3000 -n bookstore
# Usuario: admin, Contraseña: (ver secrets)

# Kibana
kubectl port-forward service/kibana-service 5601:5601 -n bookstore
```

## Comandos Útiles

### Verificar Estado
```bash
# Ver todos los pods
kubectl get pods -n bookstore

# Ver servicios
kubectl get services -n bookstore

# Ver StatefulSets
kubectl get statefulsets -n bookstore

# Ver HPA
kubectl get hpa -n bookstore
```

### Logs
```bash
# Logs de un pod específico
kubectl logs <pod-name> -n bookstore

# Logs con seguimiento
kubectl logs -f <pod-name> -n bookstore

# Logs de todos los pods de un servicio
kubectl logs -l app=payment-service-python -n bookstore
```

### Escalado
```bash
# Escalar manualmente
kubectl scale deployment payment-service-python --replicas=3 -n bookstore

# Ver métricas de HPA
kubectl describe hpa payment-service-python-hpa -n bookstore
```

### Debugging
```bash
# Ejecutar shell en un pod
kubectl exec -it <pod-name> -n bookstore -- /bin/bash

# Describir un pod
kubectl describe pod <pod-name> -n bookstore

# Ver eventos
kubectl get events -n bookstore --sort-by='.lastTimestamp'
```

## Configuración de Recursos

### Límites de Recursos
- **CPU**: 250m - 1000m por pod
- **Memoria**: 256Mi - 2Gi por pod
- **Almacenamiento**: 5Gi - 20Gi por StatefulSet

### Escalado Automático
- **Mínimo**: 2 réplicas por servicio
- **Máximo**: 10 réplicas por servicio
- **Umbral CPU**: 70%
- **Umbral Memoria**: 80%

## Monitoreo y Alertas

### Métricas Clave
- Tasa de requests por segundo
- Tiempo de respuesta (p50, p95, p99)
- Tasa de errores (4xx, 5xx)
- Uso de CPU y memoria
- Estado de circuit breakers

### Alertas Configuradas
- Alta tasa de errores (>10%)
- Alto tiempo de respuesta (>1s)
- Servicios caídos
- Alto uso de memoria (>80%)
- Alto uso de CPU (>80%)

## Troubleshooting

### Problemas Comunes

1. **Pods en estado Pending**
   - Verificar recursos disponibles
   - Revisar affinity rules
   - Verificar PersistentVolumeClaims

2. **Pods en estado CrashLoopBackOff**
   - Revisar logs del pod
   - Verificar configuración de variables de entorno
   - Verificar health checks

3. **Circuit Breakers abiertos**
   - Revisar logs de errores
   - Verificar conectividad de red
   - Revisar configuración de timeouts

4. **Problemas de conectividad**
   - Verificar servicios y endpoints
   - Revisar configuración de red
   - Verificar DNS interno

## Próximos Pasos

1. **Implementar CI/CD** con GitHub Actions o GitLab CI
2. **Configurar Network Policies** para seguridad de red
3. **Implementar RBAC** para control de acceso
4. **Agregar más métricas** personalizadas
5. **Implementar distributed tracing** con Jaeger
6. **Configurar backup automático** de bases de datos
7. **Implementar blue-green deployments**
8. **Agregar tests de carga** automatizados