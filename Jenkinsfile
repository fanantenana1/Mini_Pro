pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_app_image"
        CONTAINER_NAME = "flask_app_container"
        PORT = "5001"
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
                script {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
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
                sleep 5
                STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/)
                if [ "$STATUS" -ne 200 ]; then
                    echo "Health check failed with status $STATUS"
                    exit 1
                fi
                echo "Health check passed with status $STATUS"
                '''
            }
        }
    }
}
