pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                dir('flask_app') {
                    sh 'docker build -t flask_hello .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('flask_app') {
                    sh 'docker run --rm flask_hello pytest test.py'
                }
            }
        }

        stage('Clean previous containers') {
            steps {
                sh '''
                # Stop and remove test container if exists
                docker ps -q --filter "name=flask_hello_test" | grep -q . && docker stop flask_hello_test || true
                docker ps -a -q --filter "name=flask_hello_test" | grep -q . && docker rm flask_hello_test || true

                # Stop and remove production container if exists
                docker ps -q --filter "name=flask_prod" | grep -q . && docker stop flask_prod || true
                docker ps -a -q --filter "name=flask_prod" | grep -q . && docker rm flask_prod || true

                # Stop and remove any container using port 5001
                CONTAINER_ID=$(docker ps -q --filter "publish=5001")
                if [ -n "$CONTAINER_ID" ]; then
                    docker stop $CONTAINER_ID
                    docker rm $CONTAINER_ID
                fi
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d --name flask_prod -p 5001:5000 flask_hello'
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
    }
}
