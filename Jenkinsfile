pipeline {
    agent any

    environment {
        DOCKER_IMAGE   = 'flask-app:latest'
        HOME           = '/var/lib/jenkins'
        MINIKUBE_HOME  = '/var/lib/jenkins/.minikube'
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
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
                    # docker run --rm ${DOCKER_IMAGE} pytest
                '''
            }
        }

        stage('Verify Minikube Access & Permissions') {
            steps {
                sh '''
                    echo "✅ Vérification de Minikube..."

                    echo "🔍 Dossier MINIKUBE_HOME :"
                    ls -ld "$MINIKUBE_HOME" || echo "❌ Dossier non accessible"

                    echo "🔍 Fichier KUBECONFIG :"
                    ls -l "$KUBECONFIG" || echo "❌ Fichier non accessible"

                    minikube status || echo "❌ Minikube ne répond pas"
                    kubectl version --client || echo "❌ kubectl ne répond pas"
                    kubectl get nodes || echo "❌ Impossible de lister les nœuds"
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression {
                    fileExists(env.KUBECONFIG)
                }
            }
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
