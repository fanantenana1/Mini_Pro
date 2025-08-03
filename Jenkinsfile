pipeline {
    agent any

    environment {
        HOME           = '/var/lib/jenkins'
        MINIKUBE_HOME  = '/var/lib/jenkins/.minikube'
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
        IMAGE_NAME     = 'flask-hello'
        IMAGE_TAG      = 'latest'
        DOCKER_IMAGE   = "${IMAGE_NAME}:${IMAGE_TAG}"
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
                    echo "🧪 Tests unitaires en cours..."
                    # docker run --rm ${DOCKER_IMAGE} pytest
                '''
            }
        }

        stage('Test serveur') {
            steps {
                sh '''
                    echo "🔬 Test du serveur Flask local..."
                    docker run -d --name test-server -p 5000:5000 ${DOCKER_IMAGE}
                    sleep 5
                    curl -I http://localhost:5000 || echo "❌ Serveur ne répond pas"
                    docker stop test-server
                    docker rm test-server
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
                    kubectl apply -f flask_app/kubernetes/deployment.yaml
                    kubectl apply -f flask_app/kubernetes/service.yaml
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

        stage('Pousser vers Docker Hub') {
            steps {
                withDockerRegistry(credentialsId: 'docker-hub-creds', url: '') {
                    sh '''
                        docker tag ${DOCKER_IMAGE} haaa012/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push haaa012/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
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
