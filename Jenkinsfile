pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "flask_hello:latest"
        DOCKERHUB_USER = "ton_dockerhub"
        KUBECONFIG = '/home/m3/.kube/config'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image in Minikube') {
            steps {
                script {
                    sh 'eval $(minikube docker-env)'
                    sh 'docker build -t ${DOCKER_IMAGE} ./flask_app'
                }
            }
        }
        stage('Test Container') {
            steps {
                sh 'docker run --rm flask_hello:latest pytest flask_app/test.py'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f flask_app/kubernetes/deployment.yaml'
                sh 'kubectl apply -f flask_app/kubernetes/service.yaml'
            }
        }
    }
    post {
        always {
            sh 'kubectl get pods'
        }
    }
}
