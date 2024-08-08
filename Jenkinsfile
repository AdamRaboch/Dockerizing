pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials-id')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/AdamRaboch/Dockerizing.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'sudo docker build -t adamrab/flask_contacts_app:latest .'
                }
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials-id', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                    sh 'docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASS'
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh 'sudo docker push adamrab/flask_contacts_app:latest'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'sudo docker-compose up -d'
            }
        }
    }
}
