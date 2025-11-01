pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "azmeerasai/flask-mysql-demo"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'  // change to your Jenkins credential id
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
          docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
        }
      }
    }

    stage('Run Tests (smoke)') {
      steps {
        script {
          // run container briefly to check health/basic endpoint
          def img = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
          img.run("-d --name temp_test -p 5000:5000")
          sleep 5
          // simple curl to endpoint on the agent (assumes agent can access localhost:5000)
          bat "curl --fail http://localhost:5000/ || (docker logs temp_test && exit 1)"
          bat "docker rm -f temp_test || true"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          docker.withRegistry('', DOCKERHUB_CREDENTIALS) {
            def built = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
            built.push()
            // optional: also push 'latest'
            built.push("latest")
          }
        }
      }
    }

    // Optional deploy stage (SSH to remote host, docker pull & run)
    stage('Deploy (optional)') {
      when { expression { return false } } // change to true or remove when enabling
      steps {
        echo "Deploy stage: add your SSH + docker-compose deploy steps here."
      }
    }
  }

  post {
    always { cleanWs() }
    failure { mail to: 'dev-team@example.com', subject: "Build failed: ${env.BUILD_URL}", body: "Build failed" }
  }
}
