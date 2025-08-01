pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_hello"
        IMAGE_TAG = "latest"
        LOCAL_REGISTRY = "localhost:4000"
        FULL_IMAGE_NAME = "${LOCAL_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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
                    docker ps -q --filter "name=flask_prod" | grep -q . && docker stop flask_prod || true
                    docker ps -a -q --filter "name=flask_prod" | grep -q . && docker rm flask_prod || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d --name flask_prod -p 5000:5000 $IMAGE_NAME'
            }
        }

        stage('Push Image to Local Registry') {
            steps {
                sh '''
                    docker tag $IMAGE_NAME $FULL_IMAGE_NAME
                    docker push $FULL_IMAGE_NAME
                '''
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                echo 'Déploiement sur Kubernetes...'
                sh 'kubectl apply -f flask_app/kubernetes/'
            }
        }

    }

    post {
        always {
            sh 'docker ps -a'
        }
    }
}
