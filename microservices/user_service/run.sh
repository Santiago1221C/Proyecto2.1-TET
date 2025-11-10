#!/bin/bash
echo "Compiling User Service..."
mvn clean compile
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

echo "Starting User Service..."
mvn spring-boot:run

