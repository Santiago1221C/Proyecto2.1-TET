FROM eclipse-temurin:23-jdk-alpine
WORKDIR /app

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN ./mvnw dependency:go-offline -B

COPY src ./src
RUN ./mvnw clean package -DskipTests

EXPOSE 8088
ENTRYPOINT ["java", "-jar", "target/gateway-0.0.1-SNAPSHOT.jar"]