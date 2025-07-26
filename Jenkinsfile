pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask_hello'
        CONTAINER_NAME = 'flask_prod'
        PORT_OUT = '5001'
        PORT_IN = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/fanantenana1/Mini_Pro.git', branch: 'main'
            }
        }

       stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask_hello ./flask_app/'
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                script {
                    sh '''
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                    '''
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name $CONTAINER_NAME -p $PORT_OUT:$PORT_IN $IMAGE_NAME'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 5' // laisser le temps au conteneur de démarrer
                sh 'curl -f http://localhost:$PORT_OUT || (echo "Flask server failed to start." && exit 1)'
            }
        }
    }
}
