pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_app_image"
        CONTAINER_NAME = "flask_app_container"
        PORT = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/fanantenana1/Mini_Pro.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('flask_app') {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }

        stage('Free Port 5000 if in use') {
            steps {
                sh '''
                PID=$(lsof -t -i:5000 || true)
                if [ ! -z "$PID" ]; then
                    echo "Port 5000 is in use by PID $PID. Killing it..."
                    kill -9 $PID || true
                fi
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}"
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 3
                STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${PORT}/ || echo 000)
                if [ "$STATUS" != "200" ]; then
                    echo "Health check failed! Got status: $STATUS"
                    exit 1
                fi
                echo "Health check passed with HTTP $STATUS"
                '''
            }
        }
    }
}
