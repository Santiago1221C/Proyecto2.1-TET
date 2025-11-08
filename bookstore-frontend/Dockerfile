# ---------- Etapa 1: Build del frontend ----------
FROM node:18-alpine AS build

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios para instalar dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Compilar la app (carpeta dist/)
RUN npm run build

# ---------- Etapa 2: Servir con Nginx ----------
FROM nginx:alpine

# Elimina la configuración por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia los archivos estáticos del build
COPY --from=build /app/dist /usr/share/nginx/html

# Copia configuración personalizada de Nginx (opcional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Comando de inicio
CMD ["nginx", "-g", "daemon off;"]