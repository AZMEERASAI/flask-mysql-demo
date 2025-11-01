pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "azmeerasai/flask-mysql-demo"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'  // update with your Jenkins credential ID
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        script {
          echo "Building Docker image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
        }
      }
    }

    stage('Run Tests (smoke)') {
      steps {
        script {
          echo "Running container for smoke tests..."

          // Ensure no old container conflicts
          bat 'docker rm -f temp_test 2>nul || exit 0'

          // Run new test container
          def img = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
          img.run("-d --name temp_test -p 5000:5000")

          // Give Flask time to start
          bat 'timeout /t 5 /nobreak'

          // Health check (endpoint test)
          bat '''
            powershell -Command "try {
              Invoke-WebRequest -Uri http://localhost:5000/ -UseBasicParsing
              Write-Host 'Health check passed'
            } catch {
              docker logs temp_test
              exit 1
            }"
          '''

          // Cleanup test container
          bat 'docker rm -f temp_test || exit 0'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          echo "Pushing Docker image to Docker Hub..."
          docker.withRegistry('', DOCKERHUB_CREDENTIALS) {
            def built = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
            built.push()
            built.push("latest")
          }
        }
      }
    }

    stage('Deploy (optional)') {
      when { expression { return false } } // change to true to enable deployment
      steps {
        echo "Deploy stage: add SSH + docker-compose deploy steps here."
      }
    }
  }

  post {
    always {
      echo "Cleaning workspace..."
      cleanWs()
    }
    failure {
      mail to: 'dev-team@example.com',
           subject: "Build failed: ${env.BUILD_URL}",
           body: "Build failed. Please check logs in Jenkins."
    }
  }
}
