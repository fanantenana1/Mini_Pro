pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "flask_hello:latest"
        KUBECONFIG = '/home/jenkins/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Use Minikube Docker') {
            steps {
                script {
                    sh 'eval $(minikube docker-env) && echo "Minikube Docker Env Activated"'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'eval $(minikube docker-env) && docker build -t ${DOCKER_IMAGE} ./flask_app'
                }
            }
        }

        stage('Test Docker Container') {
            steps {
                script {
                    sh 'eval $(minikube docker-env) && docker run --rm ${DOCKER_IMAGE} pytest flask_app/test.py'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'kubectl apply -f flask_app/kubernetes/deployment.yaml'
                    sh 'kubectl apply -f flask_app/kubernetes/service.yaml'
                }
            }
        }
    }

    post {
        always {
            script {
                // S'affiche même si le pipeline échoue
                sh 'kubectl get pods'
            }
        }
    }
}
