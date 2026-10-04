targetScope = 'resourceGroup'

@description('Azure region for all resources.')
param location string

@description('Name of the customer Azure Function App.')
param functionAppName string

@description('Name of the Order API Linux Web App for Containers.')
param orderWebAppName string

@description('Globally unique name of the Azure Container Registry.')
param acrName string

@description('Globally unique name of the Function App storage account.')
param storageAccountName string

@description('Name of the Linux App Service plan hosting the Order API.')
param orderAppServicePlanName string

@description('Name of the Flex Consumption plan hosting the Function App.')
param functionAppServicePlanName string = '${functionAppName}-plan'

@description('SKU name for the Order API App Service plan.')
param orderAppServicePlanSkuName string = 'B1'

@description('SKU tier for the Order API App Service plan.')
param orderAppServicePlanSkuTier string = 'Basic'

@description('Tags applied to all supported resources.')
param tags object = {}

var acrPullRoleDefinitionId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'

resource functionStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Enabled'
    supportsHttpsTrafficOnly: true
  }
}

resource functionPlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: functionAppServicePlanName
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: 'FC1'
    tier: 'FlexConsumption'
  }
  properties: {
    reserved: true
  }
}

resource customerFunction 'Microsoft.Web/sites@2024-04-01' = {
  name: functionAppName
  location: location
  tags: tags
  kind: 'functionapp,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    httpsOnly: true
    serverFarmId: functionPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${functionStorage.name};AccountKey=${functionStorage.listKeys().keys[0].value};EndpointSuffix=${environment().suffixes.storage}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
    }
  }
}

resource orderPlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: orderAppServicePlanName
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: orderAppServicePlanSkuName
    tier: orderAppServicePlanSkuTier
  }
  properties: {
    reserved: true
  }
}

resource orderApi 'Microsoft.Web/sites@2024-04-01' = {
  name: orderWebAppName
  location: location
  tags: tags
  kind: 'app,linux,container'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    httpsOnly: true
    serverFarmId: orderPlan.id
    siteConfig: {
      acrUseManagedIdentityCreds: true
      alwaysOn: true
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
  }
}

resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  tags: tags
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Enabled'
  }
}

resource orderApiAcrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(registry.id, orderApi.id, acrPullRoleDefinitionId)
  scope: registry
  properties: {
    principalId: orderApi.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleDefinitionId)
  }
}

output functionAppHostName string = customerFunction.properties.defaultHostName
output orderWebAppHostName string = orderApi.properties.defaultHostName
output registryLoginServer string = registry.properties.loginServer