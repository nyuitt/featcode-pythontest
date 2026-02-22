import Keycloak from 'keycloak-js'

// Singleton: ensure only one Keycloak instance ever exists across hot reloads
const keycloak = new Keycloak({
    url: 'http://localhost:8081',
    realm: 'featcode',
    clientId: 'featcode-frontend',
})

export default keycloak
