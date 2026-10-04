# Production Infrastructure

`main.bicep` creates or updates the resources required for the customer Function API and Order API Web App.

The template is idempotent: a repeated deployment reconciles the declared configuration for resources with the same names. It does not delete undeclared resources.

The deployment creates a storage account, Flex Consumption Function App, Linux App Service plan, Linux Web App for Containers, Azure Container Registry, system-assigned identities, and the Web App's `AcrPull` role assignment.

The application deployment workflow publishes the Function source and replaces the Web App container image after infrastructure is available.