pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask_app_image'
        CONTAINER_NAME = 'flask_app_container'
        HOST_PORT = '5001' // port libre sur l'hôte
        CONTAINER_PORT = '5000' // port interne du container (Flask)
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout du repo Git principal
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('flask_app') {
                    // Build de l'image Docker depuis le dossier flask_app
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                script {
                    // On essaye d'arrêter le container s'il existe (ignore erreur si non trouvé)
                    sh "docker stop ${CONTAINER_NAME} || true"
                    // On essaye de supprimer le container s'il existe (ignore erreur si non trouvé)
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Free Port if in Use') {
            steps {
                script {
                    // Vérifier si un processus écoute sur le port, le tuer
                    def portCheck = sh(script: "lsof -t -i:${HOST_PORT} || true", returnStdout: true).trim()
                    if (portCheck) {
                        echo "Port ${HOST_PORT} is in use by PID(s): ${portCheck}, killing..."
                        sh "kill -9 ${portCheck}"
                    } else {
                        echo "Port ${HOST_PORT} is free."
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                // Lancement du container avec mapping sur HOST_PORT
                sh "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}"
            }
        }

        stage('Health Check') {
            steps {
                script {
                    // Test simple de la disponibilité de l'app Flask
                    def status = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${HOST_PORT}", returnStdout: true).trim()
                    if (status == '200') {
                        echo "Health Check passed: app is reachable"
                    } else {
                        error "Health Check failed: app returned status ${status}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded, Docker container running on port ${HOST_PORT}"
        }
        failure {
            echo "❌ Pipeline failed, please check logs and fix errors."
        }
        always {
            // Optionnel: nettoyer workspace si besoin
            cleanWs()
        }
    }
}
