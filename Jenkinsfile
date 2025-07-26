pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask_hello'
        CONTAINER_NAME = 'flask_prod'
        HOST_PORT = '5001'
        CONTAINER_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/fanantenana1/Mini_Pro.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE Mini_Pro/flask_app/'
                }
            }
        }

        stage('Stop and Remove Old Container') {
            steps {
                script {
                    sh '''
                    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
                        echo "Stopping running container..."
                        docker stop $CONTAINER_NAME
                    fi

                    if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
                        echo "Removing old container..."
                        docker rm $CONTAINER_NAME
                    fi
                    '''
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh '''
                    docker run -d -p $HOST_PORT:$CONTAINER_PORT --name $CONTAINER_NAME $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Post-Run Check') {
            steps {
                script {
                    sh 'docker ps -f name=$CONTAINER_NAME'
                }
            }
        }
    }
}
