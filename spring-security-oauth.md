
# OAuth 2.0 provider

> The OAuth 2.0 provider mechanism is responsible for exposing OAuth 2.0 protected resources. 

> The provider does this by managing and verifying the OAuth 2.0 tokens used to access the protected resources.

通过令牌验证来限制对于受保护资源的访问

> The provider role in OAuth 2.0 is actually split between Authorization Service and Resource Service, 
> and while these sometimes reside in the same application, 
> with Spring Security OAuth you have the option to split them across two applications, 
> and also to have multiple Resource Services that share an Authorization Service. 
> The requests for the tokens are handled by Spring MVC controller endpoints, 
> and access to protected resources is handled by standard Spring Security request filters. 
> The following endpoints are required in the Spring Security filter chain in order to implement OAuth 2.0 Authorization Server:

Provider 的角色实际上可分为 认证服务 Authorization Service 和资源服务 Resource Service

* AuthorizationEndpoint is used to service requests for authorization. Default URL: /oauth/authorize.
* TokenEndpoint is used to service requests for access tokens. Default URL: /oauth/token.

> The following filter is required to implement an OAuth 2.0 Resource Server:

> The OAuth2AuthenticationProcessingFilter is used to load the Authentication for the request given an authenticated access token.

> For all the OAuth 2.0 provider features, configuration is simplified using special Spring OAuth @Configuration adapters. 

# Authorization Server Configuration
