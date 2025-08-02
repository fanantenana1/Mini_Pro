pipeline {
    agent any

    environment {
        APP_DIR     = "flask_hello"
        IMAGE_NAME  = "flask_hello:${env.BUILD_NUMBER}"
        TAR_FILE    = "flask_hello_${env.BUILD_NUMBER}.tar"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Clonage du dépôt..."
                git 'https://github.com/sandoche/hello-python-flask'
            }
        }

        stage('Build') {
            steps {
                dir("${APP_DIR}") {
                    echo "🏗️ Construction de l’image Docker: ${IMAGE_NAME}"
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Test') {
            steps {
                dir("${APP_DIR}") {
                    echo "✅ Exécution des tests"
                    sh "docker run --rm ${IMAGE_NAME} python3 test.py"
                }
            }
        }

        stage('Export Docker Image') {
            steps {
                dir("${APP_DIR}") {
                    echo "📦 Export de l’image Docker vers un fichier tar"
                    sh "docker save ${IMAGE_NAME} -o ${TAR_FILE}"
                }
            }
        }

        stage('Load into Minikube') {
            steps {
                dir("${APP_DIR}") {
                    echo "📤 Chargement de l’image dans Minikube"
                    sh "minikube image load ${TAR_FILE}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                dir("${APP_DIR}") {
                    echo "🚀 Déploiement sur Kubernetes avec kubectl"
                    sh '''
                        kubectl delete -f deployment.yml || true
                        kubectl apply -f deployment.yml
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "🔍 Vérification du déploiement"
                sh "kubectl get pods"
                sh "kubectl get svc"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline exécuté avec succès"
        }
        failure {
            echo "❌ Le pipeline a échoué"
        }
    }
}
