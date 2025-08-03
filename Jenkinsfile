pipeline {
    agent any
    environment {
        HOME = '/var/lib/jenkins'
        MINIKUBE_HOME = '/var/lib/jenkins/.minikube'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        IMAGE_NAME = 'flask-hello'
        IMAGE_TAG = "v${BUILD_ID}"
        DOCKER_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        DOCKER_HUB = "haaa012/${DOCKER_IMAGE}"
        SONARQUBE_ENV = 'sonar'
        SONAR_TOKEN = credentials('sonar-token')
        MAVEN_HOME = tool name: 'maven', type: 'maven'
        NEXUS_REPO = 'http://localhost:8082'
        NEXUS_CREDS = 'nexus-creds'
        PATH = "/opt/sonar-scanner/bin:$PATH"
    }

    stages {

        stage('Récupération du code source') {
            steps {
                echo 'Étape 1 : Clonage du dépôt source'
                checkout scm
            }
        }

        stage('Vérification du scanner SonarQube') {
            steps {
                echo 'Étape 2 : Vérification de la disponibilité du scanner SonarQube'
                sh 'sonar-scanner -v || echo "Scanner Sonar introuvable"'
            }
        }

        stage('Analyse statique du code') {
            when {
                expression { fileExists('flask_app/.sonar-project.properties') }
            }
            steps {
                echo 'Étape 3 : Analyse du code avec SonarQube'
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    dir('flask_app') {
                        sh "sonar-scanner -Dsonar.login=${SONAR_TOKEN} || echo 'Analyse échouée'"
                    }
                }
            }
        }

        // --- Nouvelle étape de sécurisation - Audit des dépendances ---
       stage('Security Audit') {
            steps {
                sh '''
                    python3 -m venv .audit-env
                    source .audit-env/bin/activate
                    pip install --upgrade pip
                    pip install pip-audit
                    pip-audit || echo "⚠️ Vulnérabilités détectées dans les dépendances"
                    deactivate
                    rm -rf .audit-env
                '''
            }
        }

        stage('Nettoyage Docker avant build') {
            steps {
                echo 'Étape 5 : Nettoyage des ressources Docker'
                sh '''
                    docker container prune -f
                    docker image prune -f
                    docker volume prune -f
                '''
            }
        }

        stage('Construction de l’image Docker') {
            steps {
                echo 'Étape 6 : Construction de l’image Docker de l’application'
                dir('flask_app') {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        // --- Nouvelle étape de sécurisation - Scan vulnérabilités image Docker ---
        stage('Scan des vulnérabilités Docker (Sécurité)') {
            steps {
                echo 'Étape 7 : Scan de sécurité de l’image Docker avec Trivy'
                sh '''
                    trivy image ${DOCKER_IMAGE} || echo "⚠️ Vulnérabilités détectées dans l’image Docker"
                '''
            }
        }

        stage('Tests unitaires') {
            steps {
                echo 'Étape 8 : Lancement des tests unitaires via Docker'
                sh "docker run --rm ${DOCKER_IMAGE} pytest || echo 'Tests échoués'"
            }
        }

        stage('Test du serveur (Flask)') {
            steps {
                echo 'Étape 9 : Déploiement local et test du serveur Flask'
                sh '''
                    docker run -d --name test-server -p 5000:5000 ${DOCKER_IMAGE} || echo "Erreur au lancement du conteneur"
                    sleep 5
                    curl -I http://localhost:5000 || echo "Serveur non réactif"
                    docker stop test-server || true
                    docker rm test-server || true
                '''
            }
        }

        stage('Vérification de l’environnement Kubernetes') {
            steps {
                echo 'Étape 10 : Vérification de Minikube et des ressources Kubernetes'
                sh '''
                    test -f "$KUBECONFIG" || exit 1
                    minikube status || exit 1
                    kubectl get nodes || exit 1
                '''
            }
        }

        stage('Déploiement sur Kubernetes') {
            steps {
                echo 'Étape 11 : Déploiement de l’application sur le cluster Kubernetes'
                sh '''
                    kubectl apply -f flask_app/kubernetes/deployment.yaml
                    kubectl apply -f flask_app/kubernetes/service.yaml
                '''
            }
        }

        stage('Publication de l’image sur Docker Hub') {
            steps {
                echo 'Étape 12 : Push de l’image Docker sur Docker Hub'
                withDockerRegistry(credentialsId: 'docker-hub-creds', url: '') {
                    sh '''
                        docker tag ${DOCKER_IMAGE} ${DOCKER_HUB}
                        docker push ${DOCKER_HUB}
                    '''
                }
            }
        }

    }

    post {
        always {
            echo 'Nettoyage post-pipeline'
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
            '''
        }
        failure {
            echo 'Pipeline échoué. Veuillez consulter les logs.'
        }
    }
}
