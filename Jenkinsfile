pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app:latest'
        MINIKUBE_HOME = '/home/m3/.minikube'
        KUBECONFIG = '/home/m3/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Debug Path') {
            steps {
                sh 'pwd && ls -la'
            }
        }

        stage('Cleanup Docker') {
            steps {
                sh '''
                    docker container prune -f
                    docker image prune -f
                    docker volume prune -f
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                dir('flask_app') {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running tests..."
                    # Ajoute ici des tests si nécessaires
                    # docker run --rm ${DOCKER_IMAGE} pytest
                '''
            }
        }

        stage('Fix Permissions') {
            steps {
                sh '''
                    echo "🔧 Correction des permissions Minikube..."
                    sudo chown -R jenkins:jenkins /home/m3/.minikube /home/m3/.kube
                '''
            }
        }

        stage('Verify Minikube & Permissions') {
            steps {
                sh '''
                    echo "✅ Vérification de Minikube..."
                    minikube status
                    kubectl version --client
                    kubectl get nodes
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    echo "🚀 Déploiement sur Minikube..."
                    kubectl apply -f flask_app/kube/deployment.yaml
                    kubectl apply -f flask_app/kube/service.yaml
                '''
            }
        }

        stage('Post-deploy Checks') {
            steps {
                sh '''
                    echo "🔍 Vérification du déploiement..."
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        always {
            echo '✔️ Pipeline terminé. Nettoyage...'
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
            '''
        }

        failure {
            echo '❌ Échec du pipeline.'
        }
    }
}
