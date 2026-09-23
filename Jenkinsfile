pipeline {
    agent any

    tools {
        maven 'maven'
        dockerTool 'docker'
    }

    environment {
        DOCKER_USER = 'mhdsylla'
        IMAGE_NAME  = 'library_management'
        IMAGE_TAG   = 'latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Récupération du code source depuis GitHub
                checkout scm
            }
        }

        stage('Build Maven') {
            steps {
                // Compilation du projet et génération de l'artefact (.jar)
                sh 'mvn clean install'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Construction de l'image mhdsylla/library_management:latest
                    sh "docker build -t \({DOCKER_USER}/\){IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    // Utilisation des identifiants 'dockerhub-creds'
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER_VAR',
                        passwordVariable: 'DOCKER_PASS_VAR'
                    )]) {
                        // Connexion sécurisée à DockerHub
                        sh "echo \$DOCKER_PASS_VAR | docker login -u \$DOCKER_USER_VAR --password-stdin"
                        
                        // Push de l'image sur le registre
                        sh "docker push \({DOCKER_USER}/\){IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }
    }

    post {
        always {
            // Déconnexion de DockerHub à la fin du pipeline
            sh 'docker logout'
        }
        success {
            echo 'Image publiée avec succès sur DockerHub !'
        }
        failure {
            echo 'Échec de la publication de l\'image Docker.'
        }
    }
}