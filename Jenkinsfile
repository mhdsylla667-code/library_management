pipeline {
    agent any

    environment {
        COMPOSE_PROJECT = "library_ci_${BUILD_NUMBER}"
        TEST_DB = "test_library_${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    pip install --quiet flake8 || true
                    flake8 addons/library_management --max-line-length=120 || true
                '''
            }
        }

        stage('Start test environment') {
            steps {
                sh '''
                    docker compose -p $COMPOSE_PROJECT up -d db
                    echo "Attente que Postgres soit prêt..."
                    sleep 10
                '''
            }
        }

        stage('Install module') {
            steps {
                sh '''
                    docker compose -p $COMPOSE_PROJECT run --rm web \
                        odoo -d $TEST_DB \
                        --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
                        -i library_management \
                        --test-tags /library_management \
                        --stop-after-init --log-level=test
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker compose -p $COMPOSE_PROJECT down -v || true
            '''
        }
        failure {
            echo "Le pipeline a échoué — voir les logs du stage concerné."
        }
        success {
            echo "Le module library_management s'installe et passe les tests avec succès."
        }
    }
}