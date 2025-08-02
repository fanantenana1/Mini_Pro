pipeline {
    agent any

    environment {
        TIMESTAMP = new Date().format("yyyyMMdd_HHmmss")
        DOCKER_IMAGE_NAME = "flask_hello:${TIMESTAMP}"
        TAR_FILE = "flask_hello_${TIMESTAMP}.tar"
        KUBECONFIG = '/home/m3/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image (local)') {
            steps {
                dir('flask_app') {
                    sh """
                        echo "🧹 Nettoyage image et archive précédente"
                        docker image rm -f ${DOCKER_IMAGE_NAME} || true
                        rm -f ${TAR_FILE}

                        echo "🐳 Construction de l'image Docker"
                        docker build -t ${DOCKER_IMAGE_NAME} .

                        echo "📦 Sauvegarde de l'image au format .tar"
                        docker save ${DOCKER_IMAGE_NAME} -o ${TAR_FILE}
                    """
                }
            }
        }

        stage('Inject image into Minikube Docker') {
            steps {
                dir('flask_app') {
                    sh """
                        echo "🔄 Injection de l'image dans Minikube..."
                        eval \$(minikube docker-env) || echo "⚠️ minikube docker-env failed"
                        docker load -i ${TAR_FILE} || echo "⚠️ docker load failed"
                    """
                }
            }
        }

        stage('Run Tests inside container') {
            steps {
                dir('flask_app') {
                    sh "docker run --rm ${DOCKER_IMAGE_NAME} pytest test.py || echo '⚠️ Tests failed'"
                }
            }
        }

        stage('Clean previous containers') {
            steps {
                sh '''
                    echo "🧹 Suppression des anciens containers"
                    docker rm -f $(docker ps -aq) || echo "No containers to remove"
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                    dir('flask_app/kubernetes') {
                        sh 'kubectl apply -f .'
                    }
                }
            }
        }
    }

    post {
        always {
            withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                sh '''
                    echo "🔍 Vérification des pods dans le cluster"
                    kubectl get pods || echo "⚠️ kubectl failed — check if Minikube is running"
                '''
            }

            sh '''
                echo "🧽 Nettoyage des ressources Docker inutilisées"
                docker image prune -f
                docker container prune -f
                docker volume prune -f

                echo "🧹 Suppression des vieux fichiers .tar"
                find flask_app/ -name "*.tar" -mtime +1 -delete
            '''
        }
    }
}
