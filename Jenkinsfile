pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/fanantenana1/Mini_Pro.git'
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
                sh 'docker run -d --name flask_prod -p 5000:5000 flask_hello'
            }
        }
    }

    post {
        always {
            sh 'docker ps -a'
        }
        cleanup {
            sh 'docker stop flask_prod || true'
            sh 'docker rm flask_prod || true'
        }
    }
}
