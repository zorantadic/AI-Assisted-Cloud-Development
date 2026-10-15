targetScope = 'subscription'

@description('Dedicated, approved disposable dev/test resource group.')
param resourceGroupName string
param location string
@minLength(3)
@maxLength(11)
param prefix string = 'aicloud'

resource lab 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: {
    project: 'AI-Assisted-Cloud-Development'
    environment: 'devtest'
  }
}

module foundation './foundation.bicep' = {
  name: 'baseline-foundation'
  scope: lab
  params: {
    location: location
    prefix: prefix
  }
}

output foundationOutputs object = foundation.outputs
