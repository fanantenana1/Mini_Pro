pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                dir('flask_app') {
                    sh 'docker build -t flask_hello .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('flask_app') {
                    sh 'docker run --rm flask_hello pytest test.py'
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Stop et supprimer le conteneur s'il existe déjà
                    sh 'docker stop flask_prod || true'
                    sh 'docker rm flask_prod || true'

                    // Lancer le conteneur avec le port mappé 5001:5000
                    sh 'docker run -d --name flask_prod -p 5001:5000 flask_hello'
                }
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
    }
}
