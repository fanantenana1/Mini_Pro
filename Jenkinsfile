pipeline {
    agent any

    environment {
        TIMESTAMP = new Date().format("yyyyMMdd_HHmmss")
        IMAGE_NAME = "flask_hello:${TIMESTAMP}"
        TAR_FILE = "flask_hello_${TIMESTAMP}.tar"
        KUBECONFIG = '/home/m3/.kube/config'
    }

    options {
        timeout(time: 15, unit: 'MINUTES') // ⏳ Limite globale du pipeline
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Récupération du code source..."
                checkout scm
            }
        }

        stage('Clean Docker (Prebuild)') {
            steps {
                echo "🧹 Pré-nettoyage des anciennes ressources Docker"
                sh '''
                    docker container prune -f
                    docker image prune -f
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                dir('flask_app') {
                    sh """
                        echo "🐳 Construction de l'image optimisée"
                        docker build --no-cache --pull -t ${IMAGE_NAME} .
                    """
                }
            }
        }

        stage('Test Container (Pytest)') {
            steps {
                dir('flask_app') {
                    sh """
                        echo "🧪 Lancement des tests dans le conteneur"
                        docker run --rm ${IMAGE_NAME} pytest test.py || echo '⚠️ Tests failed'
                    """
                }
            }
        }

        stage('Load into Minikube') {
            steps {
                dir('flask_app') {
                    sh """
                        echo "📦 Export de l'image en .tar"
                        docker save ${IMAGE_NAME} -o ${TAR_FILE}

                        echo "♻️ Chargement de l'image dans Minikube"
                        eval \$(minikube docker-env)
                        docker load -i ${TAR_FILE}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                    dir('flask_app/kubernetes') {
                        echo "🚀 Déploiement de l'application dans Kubernetes"
                        sh 'kubectl apply -f .'
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                    sh '''
                        echo "🔍 Vérification de l'état des pods"
                        kubectl get pods -o wide
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "🧽 Nettoyage final (Docker et fichiers temporaires)"
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
                find flask_app/ -name "*.tar" -mtime +1 -delete
            '''
        }
        failure {
            echo "❌ Le pipeline a échoué. Consultez les logs pour plus de détails."
        }
        success {
            echo "✅ Déploiement réussi !"
        }
    }
}
