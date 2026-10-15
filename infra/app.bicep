targetScope = 'resourceGroup'
param location string = resourceGroup().location
param appName string = 'aicloud-order-api'
param environmentName string
param identityName string
param registryServer string
@description('Existing immutable image reference, for example registry.azurecr.io/order-api:commit-sha')
param image string
resource environment 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: environmentName
}
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: identityName
}
resource api 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8000
        transport: 'http'
        allowInsecure: false
      }
      registries: [{
          server: registryServer
          identity: identity.id
        }]
    }
    template: {
      containers: [{
        name: 'order-api'
        image: image
        env: [{
          name: 'APP_ENVIRONMENT'
          value: 'devtest'
        }]
        resources: {
          cpu: json('0.25')
          memory: '0.5Gi'
        }
        probes: [{
          type: 'Readiness'
          httpGet: {
            path: '/health'
            port: 8000
          }
          initialDelaySeconds: 5
          periodSeconds: 10
        }]
      }]
      scale: {
        minReplicas: 0
        maxReplicas: 1
      }
    }
  }
}
output baseUrl string = 'https://${api.properties.configuration.ingress.fqdn}'
