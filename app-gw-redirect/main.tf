provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "app-rg" {
  name     = "app-rg"
  location = "SoutheastAsia"
}

resource "azurerm_virtual_network" "app-rg" {
  name                = "appgw-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.app-rg.location
  resource_group_name = azurerm_resource_group.app-rg.name
}

resource "azurerm_subnet" "app-rg" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.app-rg.name
  virtual_network_name = azurerm_virtual_network.app-rg.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "app-rg" {
  name                = "app-rg-public-ip"
  location            = azurerm_resource_group.app-rg.location
  resource_group_name = azurerm_resource_group.app-rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_application_gateway" "app-rg" {
  name                = "app-rg-appgw"
  resource_group_name = azurerm_resource_group.app-rg.name
  location            = azurerm_resource_group.app-rg.location
  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 1
  }

  gateway_ip_configuration {
    name      = "app-rg-gateway-ip"
    subnet_id = azurerm_subnet.app-rg.id
  }

  frontend_port {
    name = "app-rg-frontend-port"
    port = 80
  }

  frontend_ip_configuration {
    name                 = "app-rg-frontend-ip"
    public_ip_address_id = azurerm_public_ip.app-rg.id
  }

  backend_address_pool {
    name = "app-rg-backend-pool"
  }

  backend_http_settings {
    name                  = "app-rg-backend-http-settings"
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 20
  }

  http_listener {
    name                           = "app-rg-http-listener"
    frontend_ip_configuration_name = "app-rg-frontend-ip"
    frontend_port_name             = "app-rg-frontend-port"
    protocol                       = "Http"
  }

  /*
  url_path_map {
    name                     = "app-rg-url-path-map"
    default_backend_address_pool_id = azurerm_application_gateway.app-rg.backend_address_pool.0.id
    default_backend_http_settings_id = azurerm_application_gateway.app-rg.backend_http_settings.0.id

    default_redirect_configuration {
      redirect_type = "Found"
      target_url    = "http://www.app-rg.com"
    }

    path_rule {
      name                   = "app-rg-path-rule"
      paths                  = ["/oldpath/*"]
      backend_address_pool_id = azurerm_application_gateway.app-rg.backend_address_pool.0.id
      backend_http_settings_id = azurerm_application_gateway.app-rg.backend_http_settings.0.id
      redirect_configuration {
        redirect_type = "Permanent"
        target_url    = "http://www.app-rg.com/newpath/{path}"
      }
    }
  }
  request_routing_rule {
    name                       = "app-rg-routing-rule"
    rule_type                  = "PathBasedRouting"
    http_listener_name         = "app-rg-http-listener"
    url_path_map_name          = "app-rg-url-path-map"
  }
  */
  request_routing_rule {
    name                       = "app-rg-routing-rule"
    priority                   = 9
    rule_type                  = "Basic"
    http_listener_name         = "app-rg-http-listener"
    backend_address_pool_name  = "app-rg-backend-pool"
    backend_http_settings_name = "app-rg-backend-http-settings"
    rewrite_rule_set_name      = "apprwrule"
  }

  rewrite_rule_set {
    name                       = "apprwrule"
    rewrite_rule {
        name                   = "rule01"
        rule_sequence          = 100
        condition {
            variable           = "var_uri_path"
            pattern            = "/webhook"
            negate             = true
        }
        url {
            components         = "path_only"
            path               = "/invalid"
        }
    }   
  } 

}
