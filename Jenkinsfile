pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_hello"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Configure Minikube Docker') {
            steps {
                sh 'eval $(minikube docker-env)'
            }
        }

        stage('Build Docker image') {
            steps {
                dir('flask_app') {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('flask_app') {
                    sh 'docker run --rm $IMAGE_NAME pytest test.py'
                }
            }
        }

        stage('Clean previous containers') {
            steps {
                sh '''
                    docker ps -q --filter "name=flask_hello_test" | grep -q . && docker stop flask_hello_test || true
                    docker ps -a -q --filter "name=flask_hello_test" | grep -q . && docker rm flask_hello_test || true
                '''
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                sh 'kubectl apply -f flask_app/kubernetes/'
            }
        }
    }

    post {
        always {
            sh 'kubectl get pods'
        }
    }
}
