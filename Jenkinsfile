pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_hello"
        CONTAINER_NAME = "flask_prod"
        HOST_PORT = "5001"
        CONTAINER_PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/fanantenana1/salama_java.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('salama_java/flask_app') {
                    script {
                        sh "docker build -t ${IMAGE_NAME} ."
                    }
                }
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                script {
                    // Forcer l'arrêt et suppression du container s'il existe
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh """
                        docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    sh 'sleep 5' // Attendre quelques secondes que le service démarre
                    sh "curl --fail http://localhost:${HOST_PORT} || (echo 'Health check failed' && exit 1)"
                }
            }
        }

    }

    post {
        success {
            echo '✅ Déploiement réussi !'
        }
        failure {
            echo '❌ Une erreur est survenue pendant le pipeline.'
        }
    }
}
